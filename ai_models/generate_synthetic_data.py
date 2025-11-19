"""
Generate synthetic plant image dataset for training
This is a placeholder - in production, use real agricultural datasets
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json
import os
from pathlib import Path
import random


def generate_plant_image(health_score=0.8, width=224, height=224):
    """
    Generate a synthetic plant image
    health_score: 0.0 (unhealthy) to 1.0 (healthy)
    """
    # Create base image (soil/background)
    img = Image.new('RGB', (width, height), color=(139, 90, 43))  # Brown soil
    
    draw = ImageDraw.Draw(img)
    
    # Draw plant stem
    stem_color = (34, 139, 34) if health_score > 0.5 else (139, 90, 43)
    stem_width = int(5 * health_score) + 2
    draw.rectangle([width//2 - stem_width//2, height//2, width//2 + stem_width//2, height], 
                   fill=stem_color)
    
    # Draw leaves (healthier = more green, more leaves)
    num_leaves = int(5 + health_score * 10)
    leaf_green = int(34 + health_score * 100)
    leaf_color = (0, leaf_green, 0)
    
    for _ in range(num_leaves):
        # Random leaf position
        x = random.randint(width//4, 3*width//4)
        y = random.randint(height//4, 3*height//4)
        size = random.randint(10, 30)
        
        # Draw leaf (ellipse)
        bbox = [x - size, y - size//2, x + size, y + size//2]
        draw.ellipse(bbox, fill=leaf_color)
    
    # Add some noise/texture
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Add yellowing for unhealthy plants
    if health_score < 0.5:
        overlay = Image.new('RGB', (width, height), (255, 255, 0))
        mask = Image.new('L', (width, height), int(50 * (1 - health_score)))
        img = Image.composite(img, overlay, mask)
    
    return img


def generate_dataset(output_dir="data/plant_images", num_samples=1000):
    """Generate synthetic dataset"""
    output_path = Path(output_dir)
    images_dir = output_path / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    labels = {}
    
    print(f"Generating {num_samples} synthetic plant images...")
    
    for i in range(num_samples):
        # Random health score
        health_score = random.uniform(0.2, 1.0)
        
        # Generate image
        img = generate_plant_image(health_score)
        
        # Save image
        img_filename = f"plant_{i:04d}.jpg"
        img_path = images_dir / img_filename
        img.save(img_path, "JPEG")
        
        # Store label
        labels[img_filename] = float(health_score)
        
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_samples} images...")
    
    # Save labels
    labels_file = output_path / "labels.json"
    with open(labels_file, 'w') as f:
        json.dump(labels, f, indent=2)
    
    print(f"Dataset generated successfully!")
    print(f"Images: {images_dir}")
    print(f"Labels: {labels_file}")
    print(f"Total samples: {num_samples}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic plant dataset")
    parser.add_argument("--output_dir", type=str, default="data/plant_images")
    parser.add_argument("--num_samples", type=int, default=1000)
    
    args = parser.parse_args()
    
    generate_dataset(
        output_dir=args.output_dir,
        num_samples=args.num_samples
    )

