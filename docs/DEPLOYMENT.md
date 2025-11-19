# SmartFarm AI - Deployment Guide

## Prerequisites / المتطلبات الأساسية

- Docker & Docker Compose installed
- At least 4GB RAM available
- 10GB free disk space

## Quick Start with Docker / البدء السريع مع Docker

### 1. Clone and Setup

```bash
git clone <repository-url>
cd SmartFarm-AI
```

### 2. Environment Configuration

Create `.env` file in project root (optional):

```env
# Database
DATABASE_URL=postgresql://smartfarm:smartfarm123@postgres:5432/smartfarm_db

# Backend
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Weather API (optional)
WEATHER_API_KEY=your-openweathermap-api-key

# Frontend
VITE_API_URL=http://localhost:8000
```

### 3. Start Services

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)
- React frontend (port 3000)
- Nginx reverse proxy (port 80)

### 4. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Nginx: http://localhost

### 5. Stop Services

```bash
docker-compose down
```

To remove volumes (database data):

```bash
docker-compose down -v
```

---

## Manual Setup / الإعداد اليدوي

### Backend Setup

1. **Install Python dependencies:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup database:**

```bash
# Create database
createdb smartfarm_db

# Or using PostgreSQL client
psql -U postgres
CREATE DATABASE smartfarm_db;
```

3. **Run migrations (if using Alembic):**

```bash
alembic upgrade head
```

4. **Start backend:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Start development server:**

```bash
npm run dev
```

---

## Production Deployment / النشر للإنتاج

### 1. Build Production Images

```bash
docker-compose -f docker-compose.prod.yml build
```

### 2. Environment Variables

Set production environment variables:

```env
DATABASE_URL=postgresql://user:password@db:5432/smartfarm_db
SECRET_KEY=<strong-random-secret-key>
WEATHER_API_KEY=<your-api-key>
```

### 3. Run Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. SSL/HTTPS Setup

For production, configure SSL certificates with Nginx:

1. Obtain SSL certificate (Let's Encrypt)
2. Update `docker/nginx.conf` with SSL configuration
3. Restart Nginx service

---

## Database Management / إدارة قاعدة البيانات

### Backup Database

```bash
docker exec smartfarm_db pg_dump -U smartfarm smartfarm_db > backup.sql
```

### Restore Database

```bash
docker exec -i smartfarm_db psql -U smartfarm smartfarm_db < backup.sql
```

### Access Database

```bash
docker exec -it smartfarm_db psql -U smartfarm smartfarm_db
```

---

## Model Training / تدريب النماذج

### 1. Generate Training Data

```bash
cd ai_models
python generate_synthetic_data.py --output_dir data/plant_images --num_samples 1000
```

### 2. Train Model

```bash
python train_plant_health.py \
    --data_dir data/plant_images \
    --epochs 50 \
    --batch_size 32 \
    --lr 0.001 \
    --save_path models/plant_health_model.pth
```

### 3. Copy Model to Backend

```bash
cp models/plant_health_model.pth ../backend/models/
```

---

## Monitoring / المراقبة

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

---

## Troubleshooting / حل المشاكل

### Port Already in Use

Change ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Database Connection Error

1. Check database is running:
```bash
docker-compose ps
```

2. Verify connection string in `.env`

3. Check database logs:
```bash
docker-compose logs postgres
```

### Frontend Can't Connect to Backend

1. Verify `VITE_API_URL` in frontend `.env`
2. Check CORS settings in backend
3. Verify backend is running

### Model Loading Errors

1. Ensure models directory exists:
```bash
mkdir -p backend/models
```

2. Copy trained models to `backend/models/`

3. Check model file permissions

---

## Scaling / التوسع

### Horizontal Scaling

Add more backend instances:

```yaml
backend:
  deploy:
    replicas: 3
```

### Load Balancing

Nginx automatically load balances between instances.

### Database Scaling

For production, consider:
- Read replicas
- Connection pooling (PgBouncer)
- Database clustering

---

## Security Checklist / قائمة الأمان

- [ ] Change default database password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Backup strategy in place
- [ ] Monitor logs for suspicious activity

---

## Backup Strategy / استراتيجية النسخ الاحتياطي

### Automated Backups

Create backup script:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec smartfarm_db pg_dump -U smartfarm smartfarm_db > backups/backup_$DATE.sql
```

### Restore from Backup

```bash
docker exec -i smartfarm_db psql -U smartfarm smartfarm_db < backups/backup_YYYYMMDD_HHMMSS.sql
```

---

## Performance Optimization / تحسين الأداء

1. **Enable caching:**
   - Redis for session storage
   - CDN for static assets

2. **Database optimization:**
   - Add indexes
   - Query optimization
   - Connection pooling

3. **Frontend optimization:**
   - Code splitting
   - Lazy loading
   - Image optimization

4. **Model optimization:**
   - Model quantization
   - Batch inference
   - GPU acceleration

