# SmartFarm AI - API Documentation

## Base URL / الرابط الأساسي

```
http://localhost:8000/api
```

## Authentication / المصادقة

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints / نقاط نهاية المصادقة

### Register User

**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "Full Name"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Login

**POST** `/auth/login`

Login and receive access token.

**Request Body (form-data):**
```
username: username
password: password123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Get Current User

**GET** `/auth/me`

Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

---

## Analysis Endpoints / نقاط نهاية التحليل

### Analyze Plant Image

**POST** `/analysis/analyze_image`

Upload and analyze a plant image.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (form-data):**
```
file: <image file>
plant_type: "tomato" (optional)
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "image_path": "uploads/abc123.jpg",
  "plant_health_score": 0.85,
  "water_needs": 2.5,
  "soil_quality": "loamy",
  "fertilizer_deficiency": {
    "nitrogen": "adequate",
    "phosphorus": "moderate"
  },
  "diseases": [],
  "pests": [],
  "recommendations": {
    "water": ["Maintain current watering schedule"],
    "fertilizer": ["Apply balanced fertilizer"],
    "care": []
  },
  "plant_type": "tomato",
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Predict Water Needs

**GET** `/analysis/predict_water`

Predict water requirements based on conditions.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `plant_type` (required): Type of plant
- `soil_moisture` (required): Soil moisture level (0.0-1.0)
- `temperature` (required): Temperature in Celsius

**Response:** `200 OK`
```json
{
  "water_needs": 2.5
}
```

---

### Detect Soil Quality

**POST** `/analysis/detect_soil`

Detect soil type and quality from image.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (form-data):**
```
file: <soil image>
```

**Response:** `200 OK`
```json
{
  "soil_type": "loamy",
  "quality_score": 0.75,
  "recommendations": "Your soil appears to be loamy. Consider testing pH levels."
}
```

---

### Get Fertilizer Recommendations

**GET** `/analysis/fertilizer`

Get fertilizer recommendations for plant type.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `plant_type` (required): Type of plant

**Response:** `200 OK`
```json
{
  "nitrogen_level": "moderate",
  "phosphorus_level": "low",
  "potassium_level": "adequate",
  "recommendations": [
    "Apply nitrogen-rich fertilizer",
    "Add phosphorus supplement"
  ]
}
```

---

### Get Pest Information

**GET** `/analysis/pests`

Get pest detection and recommendations.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `plant_type` (required): Type of plant

**Response:** `200 OK`
```json
{
  "detected_pests": ["aphids", "spider_mites"],
  "risk_level": "moderate",
  "recommendations": [
    "Monitor plants regularly",
    "Use organic pest control methods"
  ]
}
```

---

### Get Analysis History

**GET** `/analysis/history`

Get user's analysis history.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 10)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "image_path": "uploads/abc123.jpg",
    "plant_health_score": 0.85,
    "water_needs": 2.5,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

## Dashboard Endpoints / نقاط نهاية لوحة التحكم

### Get Dashboard Statistics

**GET** `/dashboard/stats`

Get dashboard summary statistics.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "total_analyses": 25,
  "avg_plant_health": 0.78,
  "total_water_saved": 45.5,
  "weekly_improvement": 5.2
}
```

---

### Get Progress Data

**GET** `/dashboard/progress`

Get progress tracking data.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `weeks` (optional): Number of weeks to retrieve (default: 8)

**Response:** `200 OK`
```json
[
  {
    "week_number": 1,
    "water_usage": 2.5,
    "fertilizer_usage": 1.8,
    "plant_health_avg": 0.75,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### Get Water Usage Chart Data

**GET** `/dashboard/charts/water-usage`

Get water usage chart data.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `days` (optional): Number of days (default: 30)

**Response:** `200 OK`
```json
{
  "labels": ["2024-01-01", "2024-01-02"],
  "values": [2.5, 2.8]
}
```

---

### Get Soil Health Chart Data

**GET** `/dashboard/charts/soil-health`

Get soil health timeline chart data.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `days` (optional): Number of days (default: 30)

**Response:** `200 OK`
```json
{
  "labels": ["2024-01-01", "2024-01-02"],
  "values": [0.75, 0.78]
}
```

---

## Reports Endpoints / نقاط نهاية التقارير

### Generate PDF Report

**GET** `/reports/generate-pdf`

Generate and download PDF report.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `days` (optional): Report period in days (default: 30)

**Response:** `200 OK`
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename=smartfarm_report_YYYYMMDD.pdf`

---

## Weather Endpoints / نقاط نهاية الطقس

### Get Current Weather

**GET** `/weather/current`

Get current weather data for location.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `location` (optional): Location string (default: "Cairo,EG")

**Response:** `200 OK`
```json
{
  "location": "Cairo,EG",
  "temperature": 25.5,
  "humidity": 60.0,
  "rainfall": 0.0,
  "wind_speed": 10.5,
  "recorded_at": "2024-01-01T00:00:00"
}
```

---

### Get Weather Recommendations

**GET** `/weather/recommendations`

Get weather-aware irrigation recommendations.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `location` (optional): Location string (default: "Cairo,EG")

**Response:** `200 OK`
```json
{
  "weather": {
    "temperature": 25.5,
    "humidity": 60.0,
    "rainfall": 0.0
  },
  "recommendations": [
    {
      "type": "water",
      "priority": "medium",
      "message": "Moderate temperature. Maintain regular watering.",
      "action": "Water in early morning."
    }
  ]
}
```

---

## Error Responses / استجابات الأخطاء

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

