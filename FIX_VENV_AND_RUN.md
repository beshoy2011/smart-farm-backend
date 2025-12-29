# 🔧 إصلاح Virtual Environment وتشغيل Backend

## المشكلة:
Virtual environment يحتوي على مسارات قديمة من مكان آخر.

## الحل:

### الطريقة 1: استخدام Python مباشرة (الأسرع)

```powershell
cd backend
python -m pip install -r requirements.txt
python migrate_add_achievements.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### الطريقة 2: إعادة إنشاء Virtual Environment

```powershell
cd backend

# حذف القديم
Remove-Item -Recurse -Force venv

# إنشاء جديد
python -m venv venv

# تفعيل
.\venv\Scripts\Activate.ps1

# تثبيت
pip install -r requirements.txt

# تحديث قاعدة البيانات
python migrate_add_achievements.py

# تشغيل
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚡ الحل السريع (بدون venv):

```powershell
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

(إذا كانت المتطلبات مثبتة بالفعل)

---

**جرب الطريقة 1 - الأسرع! 🚀**


