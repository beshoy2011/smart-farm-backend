# ⚡ تشغيل سريع - Quick Start

## 🚀 خطوات سريعة

### 1️⃣ Backend (Terminal 1)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python migrate_add_achievements.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2️⃣ Frontend (Terminal 2 - جديد)

```powershell
cd frontend
npm install
npm run dev
```

---

## ✅ التحقق

- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:3000
- ✅ API Docs: http://localhost:8000/docs

---

## ⚠️ ملاحظات

1. **يجب الانتقال لمجلد `frontend` أولاً** قبل `npm run dev`
2. **يجب الانتقال لمجلد `backend` أولاً** قبل `uvicorn`
3. **استخدم terminal منفصل** لكل واحد

---

## 🐛 حل المشاكل

### إذا ظهر "package.json not found":
```powershell
# تأكد أنك في مجلد frontend
cd frontend
npm run dev
```

### إذا ظهر "Module not found":
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

**جاهز! افتح http://localhost:3000 🎉**


