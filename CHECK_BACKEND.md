# 🔍 فحص Backend - Check Backend Status

## المشكلة: 500 Internal Server Error

إذا ظهرت أخطاء 500 عند تسجيل الدخول، اتبع الخطوات التالية:

---

## 1️⃣ تأكد من أن Backend يعمل

افتح PowerShell جديد:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

يجب أن ترى:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## 2️⃣ تحقق من الأخطاء في Terminal

إذا ظهرت أخطاء في terminal الـ Backend، اقرأها وأخبرني بها.

---

## 3️⃣ تحديث قاعدة البيانات

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python migrate_add_achievements.py
```

---

## 4️⃣ تثبيت المتطلبات الجديدة

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 5️⃣ اختبار API مباشرة

افتح المتصفح:
- http://localhost:8000/docs
- جرب endpoint `/api/health`

---

## 🐛 الأخطاء الشائعة

### خطأ: "Module not found"
```powershell
pip install -r requirements.txt
```

### خطأ: "Table doesn't exist"
```powershell
python migrate_add_achievements.py
```

### خطأ: "Port already in use"
```powershell
# استخدم port آخر
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

---

## ✅ الحل السريع

1. أوقف Backend (Ctrl+C)
2. شغّل:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python migrate_add_achievements.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. افتح http://localhost:8000/docs للتأكد


