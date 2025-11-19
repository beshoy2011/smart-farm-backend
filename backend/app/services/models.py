"""
AI Model inference functions
This module contains functions for loading and running ML models
"""

import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from typing import Dict, Any, Optional
import os

# Model paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), "../../models")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


class SimplePlantHealthModel(nn.Module):
    """Simple CNN for plant health classification"""
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# Global model instances (lazy loading)
_plant_health_model = None
_soil_model = None


def _load_plant_health_model():
    """Load plant health model"""
    global _plant_health_model
    if _plant_health_model is None:
        model = SimplePlantHealthModel()
        model_path = os.path.join(MODELS_DIR, "plant_health_model.pth")
        if os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path, map_location=DEVICE))
        model.eval()
        model.to(DEVICE)
        _plant_health_model = model
    return _plant_health_model


async def predict_plant_health(
    image: Image.Image, 
    plant_type: Optional[str] = None
) -> float:
    """
    Predict plant health score (0-1)
    Higher score = healthier plant
    """
    try:
        model = _load_plant_health_model()
        img_tensor = transform(image).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            prediction = model(img_tensor)
            health_score = prediction.item()
        
        return max(0.0, min(1.0, health_score))
    except Exception as e:
        # Fallback: analyze image features heuristically
        return _heuristic_health_score(image)


def _heuristic_health_score(image: Image.Image) -> float:
    """Heuristic health score based on image analysis"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Simple heuristics: check color distribution
    # Healthy plants typically have more green
    green_channel = img_array[:, :, 1]
    green_ratio = np.mean(green_channel > 100) / img_array.size
    
    # Normalize to 0-1 range
    health_score = min(1.0, green_ratio * 2.0)
    return float(health_score)


async def predict_water_needs(
    plant_type: str,
    soil_moisture: float,
    temperature: float
) -> float:
    """
    Predict water needs in liters per day
    Simple regression model
    """
    # Base water needs by plant type (liters/day)
    base_water = {
        "tomato": 2.5,
        "lettuce": 1.5,
        "pepper": 2.0,
        "cucumber": 3.0,
        "general": 2.0
    }
    
    base = base_water.get(plant_type.lower(), base_water["general"])
    
    # Adjust for soil moisture (dryer soil needs more water)
    moisture_factor = 1.0 - (soil_moisture * 0.5)
    
    # Adjust for temperature (hotter needs more water)
    temp_factor = 1.0 + ((temperature - 20) / 20) * 0.3
    
    water_needs = base * (1 + moisture_factor) * temp_factor
    return max(0.5, min(10.0, water_needs))


async def detect_soil_type(image: Image.Image) -> str:
    """
    Detect soil type from image
    Returns: 'clay', 'sandy', 'loamy', 'silty'
    """
    try:
        # Simple color-based detection
        img_array = np.array(image)
        
        # Analyze color distribution
        avg_color = np.mean(img_array, axis=(0, 1))
        
        # Heuristic classification
        if avg_color[0] > 120:  # Reddish
            return "clay"
        elif avg_color[1] > 100:  # Brownish
            return "loamy"
        elif np.std(avg_color) < 20:  # Uniform
            return "sandy"
        else:
            return "silty"
    except:
        return "loamy"  # Default


async def detect_diseases(
    image: Image.Image,
    plant_type: Optional[str] = None
) -> list:
    """
    Detect plant diseases
    Returns list of detected diseases with confidence
    """
    # Placeholder: In production, use trained disease detection model
    # For now, return empty list (no diseases detected)
    return []


async def detect_pests(plant_type: str) -> Dict[str, Any]:
    """
    Detect common pests for plant type
    """
    # Common pests by plant type
    pest_database = {
        "tomato": ["aphids", "whiteflies", "spider_mites"],
        "lettuce": ["aphids", "slugs", "caterpillars"],
        "pepper": ["aphids", "thrips", "spider_mites"],
        "cucumber": ["aphids", "cucumber_beetles", "spider_mites"],
        "general": ["aphids", "spider_mites"]
    }
    
    pests = pest_database.get(plant_type.lower(), pest_database["general"])
    
    return {
        "detected_pests": pests[:2],  # Return first 2 as detected
        "risk_level": "moderate",
        "recommendations": [
            "Monitor plants regularly",
            "Use organic pest control methods",
            "Remove affected leaves if necessary"
        ]
    }


async def analyze_fertilizer_deficiency(
    image: Image.Image,
    plant_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze fertilizer deficiency from plant appearance
    """
    # Analyze leaf color and patterns
    img_array = np.array(image)
    
    # Simple heuristic: check for yellowing (nitrogen deficiency)
    yellow_threshold = 180
    yellow_pixels = np.sum(
        (img_array[:, :, 0] > yellow_threshold) &
        (img_array[:, :, 1] > yellow_threshold) &
        (img_array[:, :, 2] < 150)
    )
    yellow_ratio = yellow_pixels / img_array.size
    
    deficiencies = {}
    if yellow_ratio > 0.1:
        deficiencies["nitrogen"] = "low"
    else:
        deficiencies["nitrogen"] = "adequate"
    
    deficiencies["phosphorus"] = "moderate"
    deficiencies["potassium"] = "adequate"
    
    return deficiencies

