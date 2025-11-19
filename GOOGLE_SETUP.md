# إعداد Google OAuth / Google OAuth Setup

## خطوات الإعداد / Setup Steps

### 1. إنشاء Google OAuth Credentials

1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. أنشئ مشروع جديد أو اختر مشروع موجود
3. اذهب إلى **APIs & Services** > **Credentials**
4. اضغط **Create Credentials** > **OAuth client ID**
5. اختر **Web application**
6. أضف **Authorized JavaScript origins**:
   - `http://localhost:3000`
   - `http://localhost:8000`
7. أضف **Authorized redirect URIs**:
   - `http://localhost:3000`
8. انسخ **Client ID**

### 2. إضافة Client ID في Frontend

أنشئ ملف `.env` في مجلد `frontend`:

```env
VITE_GOOGLE_CLIENT_ID=your-google-client-id-here
```

### 3. تثبيت الحزم

**Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

**Frontend:**
```bash
cd frontend
npm install @react-oauth/google
```

### 4. إعادة تشغيل السيرفرات

أعد تشغيل Backend و Frontend بعد إضافة Client ID.

---

## ملاحظات / Notes

- Google OAuth يعمل فقط مع HTTPS في الإنتاج
- للتطوير المحلي، استخدم `http://localhost`
- تأكد من أن Client ID صحيح في ملف `.env`

