# كيفية تشغيل المشروع / How to Run the Project

## 🚀 الطريقة السريعة / Quick Start

### الخطوة 1: تشغيل Backend / Step 1: Start Backend

افتح **Terminal/PowerShell** في مجلد المشروع:

```powershell
# الانتقال لمجلد Backend
cd backend

# تفعيل البيئة الافتراضية
.\venv\Scripts\Activate.ps1

# تشغيل السيرفر
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend سيعمل على: **http://localhost:8000**

---

### الخطوة 2: تشغيل Frontend / Step 2: Start Frontend

افتح **Terminal/PowerShell جديد** في مجلد المشروع:

```powershell
# الانتقال لمجلد Frontend
cd frontend

# تثبيت الحزم (فقط أول مرة)
npm install

# تشغيل السيرفر
npm run dev
```

✅ Frontend سيعمل على: **http://localhost:3000**

---

## 📝 ملاحظات مهمة / Important Notes

1. **يجب تشغيل Backend أولاً** / **Backend must run first**
2. **استخدم terminal منفصل لكل واحد** / **Use separate terminal for each**
3. **Backend يستخدم SQLite** (لا يحتاج PostgreSQL) / **Backend uses SQLite** (no PostgreSQL needed)

---

## 🌐 الوصول للتطبيق / Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🎯 طريقة سريعة / Quick Method

يمكنك استخدام ملفات PowerShell الجاهزة:

### تشغيل كل شيء معاً / Start Everything:
```powershell
.\start-all.ps1
```

### أو تشغيل كل واحد على حدة / Or Start Separately:
```powershell
# Backend فقط
.\start-backend.ps1

# Frontend فقط
.\start-frontend.ps1
```

---

## ⚠️ حل المشاكل / Troubleshooting

### إذا كان Port 8000 مستخدم:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### إذا كان Port 3000 مستخدم:
عدّل `frontend/vite.config.js`:
```javascript
server: {
  port: 3001,  // غيّر الرقم
}
```

### إذا واجهت مشكلة "vite is not recognized":
```powershell
cd frontend
npm install --include=dev
```

