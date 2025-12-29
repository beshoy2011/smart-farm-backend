# 🚀 شغّل Backend الآن - Start Backend Now

## المشكلة:
Backend لا يعمل - لذلك تسجيل الدخول يفشل.

## الحل:

### افتح PowerShell جديد واكتب:

```powershell
cd "C:\Users\besho\OneDrive\Desktop\SmartFarm AI\backend"
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## يجب أن ترى:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     Started reloader process
```

---

## بعد تشغيل Backend:

1. ✅ Backend يعمل على http://localhost:8000
2. ✅ Frontend يعمل على http://localhost:3000
3. ✅ جرب تسجيل الدخول الآن - سيعمل!

---

## ملاحظة:

- **يجب أن يكون Backend و Frontend يعملان معاً**
- **Terminal 1:** Backend (port 8000)
- **Terminal 2:** Frontend (port 3000)

---

**شغّل Backend الآن! 🚀**


