"""
Authentication routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.database import get_db
from app import models, schemas, auth
import os
import httpx
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, EmailStr

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


@router.post("/register", response_model=schemas.Token)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return access token"""
    try:
        # Check if user exists
        db_user = auth.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        db_user = auth.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        if not user.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )
        if not user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is required"
            )
        
        # Validate password strength
        if len(user.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
        
        # Bcrypt has a 72-byte limit
        if len(user.password.encode('utf-8')) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be 72 characters or less"
            )
        
        import re
        if not re.search(r'[A-Z]', user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter"
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one special character"
            )
        
        try:
            hashed_password = auth.get_password_hash(user.password)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error hashing password: {str(e)}"
            )
        
        db_user = models.User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create access token for the new user
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    try:
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.username:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User missing username"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/google", response_model=schemas.Token)
async def google_auth(token_data: schemas.GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate with Google OAuth token"""
    try:
        # Verify Google token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token_data.access_token}"}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google token"
                )
            google_user = response.json()
        
        google_id = google_user.get("id")
        email = google_user.get("email")
        full_name = google_user.get("name")
        profile_picture = google_user.get("picture")
        
        # Check if user exists by Google ID
        db_user = db.query(models.User).filter(models.User.google_id == google_id).first()
        
        if not db_user:
            # Check if user exists by email
            db_user = auth.get_user_by_email(db, email=email)
            if db_user:
                # Link Google account to existing user
                db_user.google_id = google_id
                db_user.profile_picture = profile_picture
                if not db_user.full_name:
                    db_user.full_name = full_name
            else:
                # Create new user
                db_user = models.User(
                    email=email,
                    username=email.split("@")[0],  # Use email prefix as username
                    full_name=full_name,
                    google_id=google_id,
                    profile_picture=profile_picture,
                    hashed_password=None  # No password for Google users
                )
                db.add(db_user)
        
        db.commit()
        db.refresh(db_user)
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": db_user.username or db_user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication failed: {str(e)}"
        )


@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """Get current user information"""
    return current_user


# Password reset schemas
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str


def send_reset_email(email: str, reset_token: str):
    """Send password reset email"""
    try:
        # Email configuration (you should move these to environment variables)
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        
        if not smtp_user or not smtp_password:
            # If email is not configured, just log the token (for development)
            print(f"\n{'='*60}")
            print(f"Password reset token for {email}: {reset_token}")
            from urllib.parse import quote
            encoded_email = quote(email, safe='')
            print(f"Reset link: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}&email={encoded_email}")
            print(f"{'='*60}\n")
            return False  # Return False to indicate email was not sent
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = "SmartFarm AI - إعادة تعيين كلمة المرور / Password Reset"
        
        # Create reset link with URL encoding
        from urllib.parse import quote
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        encoded_email = quote(email, safe='')
        reset_link = f"{frontend_url}/reset-password?token={reset_token}&email={encoded_email}"
        
        # Email body (HTML format for better appearance)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                .button:hover {{ background: #059669; }}
                .footer {{ text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px; }}
                .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SmartFarm AI</h1>
                    <p>إعادة تعيين كلمة المرور / Password Reset</p>
                </div>
                <div class="content">
                    <p>مرحباً / Hello,</p>
                    
                    <p>لقد طلبت إعادة تعيين كلمة المرور لحسابك في SmartFarm AI.</p>
                    <p>You requested to reset your password for your SmartFarm AI account.</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">إعادة تعيين كلمة المرور / Reset Password</a>
                    </div>
                    
                    <p>أو انسخ الرابط التالي في المتصفح:</p>
                    <p>Or copy the following link to your browser:</p>
                    <p style="word-break: break-all; background: #e5e7eb; padding: 10px; border-radius: 5px; font-size: 12px;">{reset_link}</p>
                    
                    <div class="warning">
                        <strong>⚠️ تحذير / Warning:</strong><br>
                        هذا الرابط سينتهي خلال ساعة واحدة.<br>
                        This link will expire in 1 hour.
                    </div>
                    
                    <p>إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذا البريد الإلكتروني.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>مع تحيات فريق SmartFarm AI</p>
                    <p>Best regards, SmartFarm AI Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
        Hello,
        
        You requested to reset your password for SmartFarm AI.
        
        Please click the following link to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        SmartFarm AI Team
        """
        
        # Attach both HTML and plain text versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Password reset email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        # For development, just log the token
        print(f"\n{'='*60}")
        print(f"Password reset token for {email}: {reset_token}")
        from urllib.parse import quote
        encoded_email = quote(email, safe='')
        print(f"Reset link: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}&email={encoded_email}")
        print(f"{'='*60}\n")
        return False  # Return False to indicate email was not sent


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send password reset email"""
    # Check if user exists
    user = auth.get_user_by_email(db, email=request.email)
    if not user:
        # Don't reveal if email exists or not for security
        return {"success": True, "message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    
    # Store reset token in user model (you might want to create a separate table for this)
    # For now, we'll store it in a simple way - in production, use a proper token table with expiration
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # Create reset link with URL encoding
    from urllib.parse import quote
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    encoded_email = quote(request.email, safe='')
    reset_link = f"{frontend_url}/reset-password?token={reset_token}&email={encoded_email}"
    
    # Send email
    email_sent = send_reset_email(request.email, reset_token)
    
    # In development mode, include the reset link in the response
    is_production = os.getenv("ENVIRONMENT") == "production"
    response_data = {
        "success": True, 
        "message": "If the email exists, a reset link has been sent"
    }
    
    # Only include reset link in development mode for testing
    if not is_production and not email_sent:
        response_data["reset_link"] = reset_link
        response_data["message"] = "Reset link generated. Check console or use the link below (development mode only)."
        print(f"\n{'='*60}")
        print(f"Password Reset Link for {request.email}:")
        print(f"{reset_link}")
        print(f"{'='*60}\n")
    
    return response_data


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using token"""
    # Find user by email
    user = auth.get_user_by_email(db, email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if token is valid
    if not user.reset_token or user.reset_token != request.reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token expired
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Validate new password
    if len(request.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Bcrypt has a 72-byte limit
    if len(request.new_password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be 72 characters or less"
        )
    
    import re
    if not re.search(r'[A-Z]', request.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', request.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one special character"
        )
    
    # Update password
    try:
        user.hashed_password = auth.get_password_hash(request.new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating password: {str(e)}"
        )
    
    return {"success": True, "message": "Password has been reset successfully"}
    
    return {"success": True, "message": "Password has been reset successfully"}

