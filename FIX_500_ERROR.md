# 🔧 إصلاح خطأ 500 - Fix 500 Error

## المشكلة:
خطأ 500 يعني أن Backend إما:
1. لا يعمل
2. يوجد خطأ في الكود
3. قاعدة البيانات لم يتم تحديثها

---

## الحل السريع:

### 1️⃣ تحقق من Backend:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python start_backend_simple.py
```

إذا ظهرت أخطاء، أصلحها أولاً.

---

### 2️⃣ تحديث قاعدة البيانات:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python migrate_add_achievements.py
```

---

### 3️⃣ تثبيت المتطلبات:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### 4️⃣ تشغيل Backend:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**يجب أن ترى:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

### 5️⃣ اختبار API:

افتح المتصفح:
- http://localhost:8000/docs
- جرب `/api/health` - يجب أن يعمل

---

## إذا استمر الخطأ 500:

### تحقق من Terminal Backend:
- اقرأ الأخطاء في terminal
- أرسل لي الخطأ المحدد

### تحقق من قاعدة البيانات:
```powershell
python migrate_add_achievements.py
```

### تحقق من المتطلبات:
```powershell
pip install -r requirements.txt
```

---

## الأخطاء الشائعة:

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Table doesn't exist"
```powershell
python migrate_add_achievements.py
```

### "Port already in use"
```powershell
# استخدم port آخر
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

---

## ✅ بعد الإصلاح:

1. Backend يعمل على http://localhost:8000
2. Frontend يعمل على http://localhost:3000
3. جرب تسجيل الدخول مرة أخرى

---

**تم إصلاح الكود! الآن شغّل Backend وستعمل! 🚀**


