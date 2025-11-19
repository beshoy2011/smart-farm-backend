# SmartFarm AI - Setup Instructions

## 🚀 Complete Setup Guide / دليل الإعداد الكامل

### Step 1: Prerequisites / المتطلبات الأساسية

Ensure you have installed:
- Docker & Docker Compose
- Git
- (Optional) Python 3.10+ and Node.js 18+ for manual setup

### Step 2: Clone Repository / استنساخ المستودع

```bash
git clone <repository-url>
cd SmartFarm-AI
```

### Step 3: Environment Configuration / إعداد البيئة

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- Change `SECRET_KEY` to a strong random string
- Add `WEATHER_API_KEY` if you want real weather data (optional)
- Adjust database credentials if needed

### Step 4: Start with Docker / البدء مع Docker

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This will start:
- ✅ PostgreSQL database
- ✅ FastAPI backend
- ✅ React frontend
- ✅ Nginx reverse proxy

### Step 5: Access Application / الوصول للتطبيق

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Nginx**: http://localhost

### Step 6: Create Account / إنشاء حساب

1. Open http://localhost:3000
2. Click "Register"
3. Fill in your details
4. Login with your credentials

### Step 7: Upload and Analyze / رفع وتحليل

1. Navigate to "Upload & Analysis"
2. Select or drag & drop a plant image
3. (Optional) Select plant type
4. Click "Analyze Image"
5. View results and recommendations

## 🔧 Manual Setup (Without Docker) / الإعداد اليدوي

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
# Create PostgreSQL database
createdb smartfarm_db

# Or using SQLite (for development)
# Update DATABASE_URL in .env to: sqlite:///./smartfarm.db

# 5. Run migrations (if using Alembic)
alembic upgrade head

# 6. Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

## 🧪 Testing / الاختبار

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🤖 Training AI Models / تدريب نماذج الذكاء الاصطناعي

### Generate Training Data

```bash
cd ai_models
python generate_synthetic_data.py \
    --output_dir data/plant_images \
    --num_samples 1000
```

### Train Model

```bash
python train_plant_health.py \
    --data_dir data/plant_images \
    --epochs 50 \
    --batch_size 32 \
    --lr 0.001 \
    --save_path models/plant_health_model.pth
```

### Copy Model to Backend

```bash
mkdir -p ../backend/models
cp models/plant_health_model.pth ../backend/models/
```

## 📊 Verify Installation / التحقق من التثبيت

### Check Backend

```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"}
```

### Check Frontend

Open http://localhost:3000 in browser - should see login page.

### Check Database

```bash
docker exec -it smartfarm_db psql -U smartfarm smartfarm_db
# Or manually: psql -U smartfarm smartfarm_db
```

## 🐛 Troubleshooting / حل المشاكل

### Port Already in Use

Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8000 to available port
```

### Database Connection Error

1. Check if PostgreSQL is running:
```bash
docker-compose ps
```

2. Verify DATABASE_URL in `.env`

3. Check database logs:
```bash
docker-compose logs postgres
```

### Frontend Can't Connect to Backend

1. Verify `VITE_API_URL` in frontend `.env`
2. Check CORS settings in backend
3. Ensure backend is running

### Model Loading Errors

1. Create models directory:
```bash
mkdir -p backend/models
```

2. Copy trained models to `backend/models/`

3. Check file permissions

## 📝 Next Steps / الخطوات التالية

1. ✅ System is running
2. ✅ Create user account
3. ✅ Upload test images
4. ✅ Explore dashboard
5. ✅ Generate reports
6. ⚠️ Train models with real data (for production)
7. ⚠️ Configure production environment variables
8. ⚠️ Set up SSL/HTTPS (for production)

## 📚 Additional Resources / موارد إضافية

- **Architecture**: See `docs/ARCHITECTURE.md`
- **API Docs**: See `docs/API_DOCUMENTATION.md`
- **Deployment**: See `docs/DEPLOYMENT.md`
- **Training**: See `docs/TRAINING_GUIDE.md`

## ✅ Verification Checklist / قائمة التحقق

- [ ] Docker services are running
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Can register new user
- [ ] Can login
- [ ] Can upload image
- [ ] Analysis returns results
- [ ] Dashboard shows data
- [ ] Reports can be generated

## 🎉 Success! / نجاح!

Your SmartFarm AI system is now running! Start analyzing plants and optimizing your agricultural practices.

---

**Need Help?** Check the documentation in `docs/` directory or open an issue.

