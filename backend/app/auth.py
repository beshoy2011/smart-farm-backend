"""
Authentication utilities
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    try:
        if not password:
            raise ValueError("Password cannot be empty")
            
        # Bcrypt has a 72-byte limit, so we need to handle longer passwords
        # We'll hash the password first with SHA256, then bcrypt the hash
        password_bytes = password.encode('utf-8')
        
        if len(password_bytes) > 72:
            # Hash with SHA256 first, then bcrypt the hash
            password_hash = hashlib.sha256(password_bytes).hexdigest()
            password_to_hash = password_hash.encode('utf-8')
        else:
            password_to_hash = password_bytes
        
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_to_hash, salt)
        return hashed.decode('utf-8')
    except Exception as e:
        print(f"Password hashing error: {e}")
        import traceback
        traceback.print_exc()
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        if not hashed_password:
            return False
            
        hashed_bytes = hashed_password.encode('utf-8')
        password_bytes = plain_password.encode('utf-8')
        
        # Try direct verification first (for normal passwords)
        try:
            if bcrypt.checkpw(password_bytes, hashed_bytes):
                return True
        except Exception:
            pass
        
        # If password is longer than 72 bytes, try hashing with SHA256 first
        # (for passwords that were hashed with SHA256 first)
        if len(password_bytes) > 72:
            try:
                password_hash = hashlib.sha256(password_bytes).hexdigest()
                password_hash_bytes = password_hash.encode('utf-8')
                if bcrypt.checkpw(password_hash_bytes, hashed_bytes):
                    return True
            except Exception:
                pass
        
        # Try with passlib for backward compatibility (if passlib is available)
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            if pwd_context.verify(plain_password, hashed_password):
                return True
        except Exception:
            pass
        
        return False
    except Exception as e:
        print(f"Password verification error: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    # Check if user has password (not a Google-only user)
    if not user.hashed_password:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        identifier: str = payload.get("sub")  # Can be username or email
        if identifier is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Try to find user by username first, then by email
    user = get_user_by_username(db, username=identifier)
    if user is None:
        user = get_user_by_email(db, email=identifier)
    
    if user is None:
        raise credentials_exception
    return user

