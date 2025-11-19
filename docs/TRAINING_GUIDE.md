# AI Models Training Guide

## Overview / نظرة عامة

This guide explains how to train the AI models used in SmartFarm AI for plant health analysis.

## Prerequisites / المتطلبات الأساسية

- Python 3.10+
- PyTorch 2.0+
- CUDA-capable GPU (recommended)
- 10GB+ free disk space for datasets

## Dataset Preparation / إعداد البيانات

### Option 1: Use Synthetic Data (for testing)

Generate synthetic plant images:

```bash
cd ai_models
python generate_synthetic_data.py \
    --output_dir data/plant_images \
    --num_samples 5000
```

### Option 2: Use Real Agricultural Datasets

Recommended datasets:

1. **PlantNet Dataset**
   - Download from: https://plantnet.org/
   - Contains plant species images

2. **Plant Village Dataset**
   - Download from: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
   - Contains plant disease images

3. **Custom Dataset**
   - Collect your own agricultural images
   - Organize by plant type and health status

### Dataset Structure

```
data/
└── plant_images/
    ├── images/
    │   ├── plant_0001.jpg
    │   ├── plant_0002.jpg
    │   └── ...
    └── labels.json
```

`labels.json` format:
```json
{
  "plant_0001.jpg": 0.85,
  "plant_0002.jpg": 0.60,
  ...
}
```

Health scores: 0.0 (unhealthy) to 1.0 (healthy)

## Training Plant Health Model / تدريب نموذج صحة النبات

### Basic Training

```bash
python train_plant_health.py \
    --data_dir data/plant_images \
    --epochs 50 \
    --batch_size 32 \
    --lr 0.001 \
    --save_path models/plant_health_model.pth
```

### Advanced Training with GPU

```bash
CUDA_VISIBLE_DEVICES=0 python train_plant_health.py \
    --data_dir data/plant_images \
    --epochs 100 \
    --batch_size 64 \
    --lr 0.0001 \
    --save_path models/plant_health_model.pth
```

### Training Parameters

- `--data_dir`: Path to dataset directory
- `--epochs`: Number of training epochs (default: 50)
- `--batch_size`: Batch size (default: 32)
- `--lr`: Learning rate (default: 0.001)
- `--save_path`: Path to save trained model

## Model Evaluation / تقييم النموذج

After training, evaluate model performance:

```python
# Load model
model = PlantHealthModel()
model.load_state_dict(torch.load('models/plant_health_model.pth'))
model.eval()

# Evaluate on test set
# Calculate accuracy, precision, recall, F1-score
```

### Target Metrics

- **Accuracy**: >85%
- **Precision**: >80%
- **Recall**: >80%
- **F1-Score**: >80%

## Model Architecture / البنية المعمارية

### Plant Health Model

```
Input: 224x224 RGB Image
  ↓
Conv Block 1: 32 filters
  ↓
Conv Block 2: 64 filters
  ↓
Conv Block 3: 128 filters
  ↓
Conv Block 4: 256 filters
  ↓
Global Average Pooling
  ↓
Fully Connected: 128 → 64 → 1
  ↓
Output: Health Score (0.0 - 1.0)
```

## Training Tips / نصائح التدريب

1. **Data Augmentation:**
   - Random horizontal flip
   - Random rotation
   - Color jitter
   - Random crop

2. **Learning Rate Scheduling:**
   - Start with 0.001
   - Reduce by 0.1 every 10 epochs
   - Use cosine annealing

3. **Regularization:**
   - Dropout (0.5)
   - Weight decay
   - Early stopping

4. **Validation:**
   - Use 80/20 train/validation split
   - Monitor validation loss
   - Save best model

## Transfer Learning / التعلم النقل

For better performance, use pre-trained models:

```python
import torchvision.models as models

# Use ResNet as backbone
backbone = models.resnet18(pretrained=True)
# Fine-tune for plant health
```

## Model Optimization / تحسين النموذج

### Quantization

Reduce model size:

```python
model_quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

### Pruning

Remove unnecessary weights:

```python
# Prune 20% of weights
torch.nn.utils.prune.global_unstructured(
    parameters_to_prune,
    pruning_method=torch.nn.utils.prune.L1Unstructured,
    amount=0.2
)
```

## Deployment / النشر

After training:

1. **Save model:**
```bash
cp models/plant_health_model.pth ../backend/models/
```

2. **Verify model loads:**
```python
from app.services.models import _load_plant_health_model
model = _load_plant_health_model()
```

3. **Test inference:**
```python
from PIL import Image
image = Image.open('test_image.jpg')
health_score = await predict_plant_health(image)
```

## Continuous Learning / التعلم المستمر

For production:

1. Collect user feedback
2. Retrain periodically with new data
3. A/B test new models
4. Monitor model performance

## Troubleshooting / حل المشاكل

### Out of Memory

- Reduce batch size
- Use gradient accumulation
- Enable mixed precision training

### Poor Performance

- Increase dataset size
- Use data augmentation
- Try transfer learning
- Tune hyperparameters

### Overfitting

- Increase dropout
- Add more regularization
- Use more training data
- Early stopping

## Resources / الموارد

- PyTorch Documentation: https://pytorch.org/docs/
- PlantNet Dataset: https://plantnet.org/
- Agricultural ML Papers: Research papers on plant disease detection

