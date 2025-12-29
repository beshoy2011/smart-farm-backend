# 🚀 دليل تشغيل المشروع - How to Run the Project

## ⚡ الطريقة السريعة (الأسهل)

### استخدام ملفات PowerShell الجاهزة:

```powershell
# تشغيل كل شيء معاً
.\start-all.ps1
```

أو تشغيل كل واحد على حدة:

```powershell
# Terminal 1 - Backend
.\start-backend.ps1

# Terminal 2 - Frontend  
.\start-frontend.ps1
```

---

## 📋 الطريقة اليدوية (خطوة بخطوة)

### الخطوة 1: تحديث قاعدة البيانات (للميزات الجديدة)

```powershell
cd backend
python migrate_add_achievements.py
```

### الخطوة 2: تشغيل Backend

افتح **PowerShell** أو **Terminal**:

```powershell
# 1. الانتقال لمجلد Backend
cd backend

# 2. تفعيل البيئة الافتراضية
.\venv\Scripts\Activate.ps1

# إذا لم تكن موجودة، أنشئها:
# python -m venv venv
# .\venv\Scripts\Activate.ps1

# 3. تثبيت المتطلبات (فقط أول مرة أو بعد إضافة ميزات جديدة)
pip install -r requirements.txt

# 4. تشغيل السيرفر
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend سيعمل على:** http://localhost:8000
✅ **API Documentation:** http://localhost:8000/docs

---

### الخطوة 3: تشغيل Frontend

افتح **PowerShell جديد** أو **Terminal جديد**:

```powershell
# 1. الانتقال لمجلد Frontend
cd frontend

# 2. تثبيت الحزم (فقط أول مرة)
npm install

# 3. تشغيل السيرفر
npm run dev
```

✅ **Frontend سيعمل على:** http://localhost:3000

---

## 🎯 الوصول للتطبيق

بعد تشغيل كل شيء:

1. **افتح المتصفح:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

2. **سجّل حساب جديد:**
   - اضغط "Register" أو "تسجيل"
   - أدخل بياناتك
   - سجّل دخول

3. **ابدأ الاستخدام:**
   - ارفع صورة نبات
   - شاهد التحليل
   - استمتع بالميزات الجديدة! 🎉

---

## ⚙️ إعدادات اختيارية

### إعداد البريد الإلكتروني (للإشعارات):

1. أنشئ ملف `.env` في مجلد `backend`:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

2. أعد تشغيل Backend

---

## 🐛 حل المشاكل الشائعة

### المشكلة 1: Port 8000 مستخدم

```powershell
# استخدم port آخر
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

ثم غيّر في `frontend/.env`:
```env
VITE_API_URL=http://localhost:8001
```

---

### المشكلة 2: Port 3000 مستخدم

عدّل `frontend/vite.config.js`:
```javascript
server: {
  port: 3001,  // غيّر الرقم
}
```

---

### المشكلة 3: "Module not found" في Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### المشكلة 4: "npm is not recognized"

1. تأكد من تثبيت Node.js: https://nodejs.org
2. أعد فتح PowerShell
3. جرب: `npm --version`

---

### المشكلة 5: WebSocket لا يعمل

1. تأكد من أن Backend يعمل على port 8000
2. تحقق من console في المتصفح (F12)
3. تأكد من CORS settings في `backend/main.py`

---

### المشكلة 6: قاعدة البيانات لا تعمل

```powershell
cd backend
python migrate_add_achievements.py
```

---

## 📝 ملاحظات مهمة

1. ✅ **يجب تشغيل Backend أولاً** قبل Frontend
2. ✅ **استخدم terminal منفصل** لكل واحد
3. ✅ **Backend يستخدم SQLite** (لا يحتاج PostgreSQL)
4. ✅ **الميزات الجديدة تعمل تلقائياً** بعد تحديث قاعدة البيانات

---

## 🎨 الميزات الجديدة المتاحة

بعد التشغيل، ستجد:

- ✅ **WebSocket** - مراقبة فورية في Dashboard
- ✅ **الإنجازات** - صفحة `/achievements`
- ✅ **البريد الإلكتروني** - إشعارات تلقائية (إذا أعددتها)
- ✅ **Push Notifications** - جاهز للتكامل

---

## ✅ قائمة التحقق

قبل البدء، تأكد من:

- [ ] Python 3.10+ مثبت
- [ ] Node.js 18+ مثبت
- [ ] Backend يعمل على http://localhost:8000
- [ ] Frontend يعمل على http://localhost:3000
- [ ] قاعدة البيانات محدثة (شغّل migration)

---

## 🎉 جاهز!

الآن المشروع يعمل! افتح http://localhost:3000 وابدأ الاستخدام.

---

## 📞 مساعدة إضافية

- راجع `IMPLEMENTATION_SUMMARY.md` للميزات الجديدة
- راجع `NEW_FEATURES_GUIDE.md` لدليل الاستخدام
- راجع `START.md` للتفاصيل الإضافية

---

**تم! استمتع بالمشروع! 🚀**


