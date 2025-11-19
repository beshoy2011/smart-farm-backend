# إعداد البريد الإلكتروني / Email Setup

## إعداد Gmail / Gmail Setup

### الخطوات / Steps:

1. **تفعيل التحقق بخطوتين / Enable 2-Step Verification:**
   - اذهب إلى: https://myaccount.google.com/security
   - فعّل "التحقق بخطوتين" / Enable "2-Step Verification"

2. **إنشاء App Password:**
   - اذهب إلى: https://myaccount.google.com/apppasswords
   - اختر "البريد" و "الكمبيوتر" / Select "Mail" and "Computer"
   - انسخ كلمة المرور التي ستظهر (16 حرف) / Copy the password that appears (16 characters)

3. **إضافة المتغيرات في ملف .env:**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   FRONTEND_URL=http://localhost:3000
   ```

4. **إعادة تشغيل الـ Backend:**
   - بعد إضافة المتغيرات، أعد تشغيل الـ backend server

## إعدادات أخرى / Other Email Providers

### Outlook/Hotmail:
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Yahoo:
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

## ملاحظات / Notes

- **لا تستخدم كلمة المرور العادية لـ Gmail** - يجب استخدام App Password
- **Do not use your regular Gmail password** - You must use an App Password
- في وضع التطوير (بدون إعدادات SMTP)، سيظهر الرابط في الـ console
- In development mode (without SMTP settings), the link will appear in the console

