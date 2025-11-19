# AI Models Training Guide

## Overview / نظرة عامة

This directory contains training scripts and models for SmartFarm AI's machine learning components.

## Models / النماذج

1. **Plant Health Classification** - CNN model to classify plant health (0-1 score)
2. **Water Needs Prediction** - Regression model for water requirements
3. **Soil Type Detection** - Classification model for soil types
4. **Disease Detection** - CNN for plant disease identification
5. **Pest Detection** - Classification model for common pests

## Training Instructions / تعليمات التدريب

### 1. Generate Synthetic Data (for testing)

```bash
python generate_synthetic_data.py --output_dir data/plant_images --num_samples 1000
```

### 2. Train Plant Health Model

```bash
python train_plant_health.py \
    --data_dir data/plant_images \
    --epochs 50 \
    --batch_size 32 \
    --lr 0.001 \
    --save_path models/plant_health_model.pth
```

### 3. Model Evaluation

After training, models are saved to `models/` directory and loaded by the inference service.

## Production Models / النماذج للإنتاج

For production use, train models on real agricultural datasets:

- **PlantNet Dataset** - Plant species identification
- **Plant Village Dataset** - Plant disease classification
- **Custom Agricultural Datasets** - Domain-specific data

## Model Architecture / البنية المعمارية

### Plant Health Model
- Input: 224x224 RGB images
- Architecture: CNN with 4 convolutional blocks
- Output: Health score (0.0 - 1.0)
- Loss: Binary Cross Entropy

### Water Prediction Model
- Input: Plant type, soil moisture, temperature
- Architecture: Simple regression
- Output: Water needs in liters/day

## Performance Metrics / مقاييس الأداء

Target metrics:
- Plant Health Accuracy: >85%
- Water Prediction MAE: <0.5L
- Soil Detection Accuracy: >80%

## Notes / ملاحظات

- Models use PyTorch
- Training requires GPU for faster convergence
- Use data augmentation for better generalization
- Regularize models to prevent overfitting

