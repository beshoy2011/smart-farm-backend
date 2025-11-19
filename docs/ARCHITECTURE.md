# SmartFarm AI - Architecture Documentation

## System Architecture / البنية المعمارية

### Overview / نظرة عامة

SmartFarm AI is a full-stack agricultural analysis platform built with modern technologies:

- **Frontend**: React 18 + Vite + TailwindCSS
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **AI/ML**: PyTorch for model inference
- **Deployment**: Docker + Docker Compose + Nginx

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Browser                       │
│                    (React + TailwindCSS)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/HTTPS
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Nginx Reverse Proxy                     │
│                    (Load Balancing)                          │
└───────┬───────────────────────────────┬───────────────────────┘
        │                               │
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│   Frontend     │            │    Backend       │
│   (React)      │            │   (FastAPI)      │
│   Port: 3000   │            │   Port: 8000    │
└────────────────┘            └────────┬─────────┘
                                       │
                                       │
                            ┌──────────▼──────────┐
                            │   PostgreSQL DB      │
                            │   Port: 5432        │
                            └─────────────────────┘
                                       │
                            ┌──────────▼──────────┐
                            │   AI Models         │
                            │   (PyTorch)         │
                            └─────────────────────┘
```

## Component Architecture / بنية المكونات

### Frontend Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── Layout.jsx
│   │   └── ResultCard.jsx
│   ├── pages/          # Page components
│   │   ├── Home.jsx
│   │   ├── Upload.jsx
│   │   ├── Dashboard.jsx
│   │   ├── PlantsLibrary.jsx
│   │   ├── Progress.jsx
│   │   ├── Reports.jsx
│   │   ├── Login.jsx
│   │   └── Register.jsx
│   ├── store/          # State management (Zustand)
│   │   └── authStore.js
│   ├── services/       # API services
│   │   └── api.js
│   └── App.jsx         # Main app component
```

### Backend Structure

```
backend/
├── app/
│   ├── routers/        # API route handlers
│   │   ├── auth.py
│   │   ├── analysis.py
│   │   ├── dashboard.py
│   │   ├── reports.py
│   │   └── weather.py
│   ├── services/       # Business logic
│   │   ├── ai_service.py
│   │   └── models.py
│   ├── models.py       # Database models
│   ├── schemas.py      # Pydantic schemas
│   ├── auth.py         # Authentication
│   └── database.py     # DB configuration
└── main.py             # FastAPI app entry
```

## Data Flow / تدفق البيانات

### Image Analysis Flow

1. User uploads image → Frontend
2. Frontend sends POST /api/analysis/analyze_image → Backend
3. Backend saves image → File system
4. Backend calls AI Service → Model inference
5. AI Service processes image → Multiple models
6. Results aggregated → Database
7. Response sent → Frontend
8. Results displayed → User

### Authentication Flow

1. User submits credentials → Frontend
2. POST /api/auth/login → Backend
3. Backend validates → Database
4. JWT token generated → Backend
5. Token returned → Frontend
6. Token stored → LocalStorage
7. Token included → All API requests

## Database Schema / مخطط قاعدة البيانات

### Tables

**users**
- id (PK)
- email (unique)
- username (unique)
- hashed_password
- full_name
- is_active
- created_at

**analyses**
- id (PK)
- user_id (FK → users)
- image_path
- plant_health_score
- water_needs
- soil_quality
- fertilizer_deficiency (JSON)
- diseases (JSON)
- pests (JSON)
- recommendations (JSON)
- plant_type
- created_at

**weather_data**
- id (PK)
- location
- temperature
- humidity
- rainfall
- wind_speed
- recorded_at

**progress_tracking**
- id (PK)
- user_id (FK → users)
- week_number
- water_usage
- fertilizer_usage
- plant_health_avg
- created_at

## AI Models / نماذج الذكاء الاصطناعي

### Model Architecture

1. **Plant Health Model**
   - Type: CNN Classification
   - Input: 224x224 RGB image
   - Output: Health score (0.0 - 1.0)
   - Architecture: 4 conv blocks + classifier

2. **Water Prediction Model**
   - Type: Regression
   - Input: Plant type, soil moisture, temperature
   - Output: Water needs (liters/day)

3. **Soil Detection Model**
   - Type: Image Classification
   - Input: Soil image
   - Output: Soil type (clay, sandy, loamy, silty)

4. **Disease Detection Model**
   - Type: CNN Classification
   - Input: Plant image
   - Output: Disease labels with confidence

5. **Pest Detection Model**
   - Type: Classification
   - Input: Plant type
   - Output: Common pests list

## API Endpoints / نقاط النهاية

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Analysis
- `POST /api/analysis/analyze_image` - Analyze plant image
- `GET /api/analysis/predict_water` - Predict water needs
- `POST /api/analysis/detect_soil` - Detect soil type
- `GET /api/analysis/fertilizer` - Get fertilizer recommendations
- `GET /api/analysis/pests` - Get pest information
- `GET /api/analysis/history` - Get analysis history

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/progress` - Get progress data
- `GET /api/dashboard/charts/water-usage` - Water usage chart data
- `GET /api/dashboard/charts/soil-health` - Soil health chart data

### Reports
- `GET /api/reports/generate-pdf` - Generate PDF report

### Weather
- `GET /api/weather/current` - Get current weather
- `GET /api/weather/recommendations` - Get weather-based recommendations

## Security / الأمان

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- File upload validation

## Deployment / النشر

### Docker Compose Services

1. **postgres** - Database service
2. **backend** - FastAPI application
3. **frontend** - React development server
4. **nginx** - Reverse proxy and load balancer

### Environment Variables

**Backend:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration

**Frontend:**
- `VITE_API_URL` - Backend API URL

## Performance Optimization / تحسين الأداء

- Model lazy loading
- Image caching
- Database query optimization
- API response caching
- Frontend code splitting
- CDN for static assets

## Scalability / قابلية التوسع

- Horizontal scaling with Docker
- Database connection pooling
- Async request handling
- Microservices-ready architecture
- Load balancing with Nginx

