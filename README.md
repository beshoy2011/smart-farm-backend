# SmartFarm AI – منصة الزراعة الذكية المتكاملة

## 🌱 Project Overview / نظرة عامة على المشروع

SmartFarm AI is an innovative agricultural technology platform that uses AI, computer vision, and weather data to optimize water usage, soil quality, fertilizer application, and plant health monitoring.

منصة SmartFarm AI هي منصة تكنولوجية زراعية مبتكرة تستخدم الذكاء الاصطناعي ورؤية الكمبيوتر وبيانات الطقس لتحسين استخدام المياه وجودة التربة وتطبيق الأسمدة ومراقبة صحة النباتات.

## 🏗️ Architecture / البنية المعمارية

```
SmartFarm-AI/
├── backend/              # FastAPI backend
├── frontend/            # React + Vite frontend
├── ai_models/           # ML model training and inference
├── docker/              # Docker configurations
├── docs/                # Documentation
└── tests/               # Integration tests
```

## 🚀 Quick Start / البدء السريع

### Prerequisites / المتطلبات الأساسية

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### Local Development / التطوير المحلي

1. **Clone and setup:**
```bash
git clone <repository-url>
cd SmartFarm-AI
```

2. **Start with Docker:**
```bash
docker-compose up --build
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup / الإعداد اليدوي

#### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 📋 Features / المميزات

- ✅ Plant image analysis with AI
- ✅ Water usage prediction
- ✅ Soil quality detection
- ✅ Fertilizer deficiency detection
- ✅ Disease and pest detection
- ✅ Weather-aware recommendations
- ✅ Dashboard and analytics
- ✅ Progress tracking
- ✅ PDF report generation

## 🤖 AI Models / نماذج الذكاء الاصطناعي

The system includes:
- Vision Transformer for plant health classification
- Regression model for water prediction
- CNN for soil type detection
- Disease and pest detection models

## 📚 Documentation / التوثيق

See `docs/` directory for:
- API Documentation
- Architecture diagrams
- Model training guide
- Deployment guide

## 🧪 Testing / الاختبار

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## 📄 License / الترخيص

MIT License

