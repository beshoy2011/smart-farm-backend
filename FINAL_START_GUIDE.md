# 🎯 الدليل النهائي لتشغيل المشروع

## ⚠️ المشكلة الحالية:
Backend لا يعمل → لذلك تسجيل الدخول يفشل

---

## ✅ الحل (3 خطوات فقط):

### الخطوة 1: شغّل Backend

**افتح PowerShell جديد** واكتب:

```powershell
.\start-backend.ps1
```

أو يدوياً:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python migrate_add_achievements.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**يجب أن ترى:**
```
✅ Virtual environment activated
📦 Installing dependencies...
📊 Updating database...
🚀 Starting server...
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

### الخطوة 2: تأكد من Frontend يعمل

في **Terminal آخر** (Frontend):

```powershell
cd frontend
npm run dev
```

**يجب أن ترى:**
```
VITE v5.4.21  ready in 2619 ms
➜  Local:   http://localhost:3000/
```

---

### الخطوة 3: جرب تسجيل الدخول

1. افتح http://localhost:3000
2. سجّل دخول
3. ✅ يجب أن يعمل الآن!

---

## 🔍 التحقق:

### Backend يعمل؟
افتح: http://localhost:8000/docs
- يجب أن ترى Swagger UI

### Frontend يعمل؟
افتح: http://localhost:3000
- يجب أن ترى صفحة تسجيل الدخول

---

## 🐛 إذا استمرت المشكلة:

### 1. تحقق من Ports:
```powershell
# Backend على port 8000
netstat -ano | findstr :8000

# Frontend على port 3000
netstat -ano | findstr :3000
```

### 2. تحقق من الأخطاء:
- اقرأ الأخطاء في terminal Backend
- اقرأ الأخطاء في terminal Frontend
- اقرأ الأخطاء في Console المتصفح (F12)

---

## 📝 ملخص:

1. ✅ **Backend يعمل** → http://localhost:8000
2. ✅ **Frontend يعمل** → http://localhost:3000
3. ✅ **تسجيل الدخول يعمل** → جرب الآن!

---

**شغّل Backend الآن وستعمل! 🚀**


