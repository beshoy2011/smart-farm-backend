# ⚡ إصلاح سريع لخطأ 500

## المشكلة:
Backend يعطي خطأ 500 عند تسجيل الدخول.

## الحل السريع:

### 1️⃣ تحقق من Backend:

افتح PowerShell في مجلد `backend`:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python test_login.py
```

إذا ظهرت أخطاء، أصلحها.

---

### 2️⃣ شغّل Backend:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**يجب أن ترى:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

### 3️⃣ تحقق من الأخطاء:

في terminal Backend، اقرأ الأخطاء التي تظهر عند محاولة تسجيل الدخول.

**الأخطاء الشائعة:**
- `Module not found` → `pip install -r requirements.txt`
- `Table doesn't exist` → `python migrate_add_achievements.py`
- `Database locked` → أعد تشغيل Backend

---

### 4️⃣ اختبار مباشر:

افتح http://localhost:8000/docs
- جرب `/api/auth/login` مباشرة
- شاهد الخطأ المحدد

---

## إذا استمر الخطأ:

1. **انسخ الخطأ الكامل** من terminal Backend
2. **أرسله لي** لأصلحه

---

**تم إضافة معالجة أخطاء أفضل! الآن شغّل Backend وسترى الخطأ المحدد! 🔍**


