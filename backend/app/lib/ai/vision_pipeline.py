"""
Vision pipeline that extracts agronomic metrics from plant images.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
)

LOGGER = logging.getLogger("smartfarm.ai.pipeline")


def _clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    """Clamp floating point values."""
    return float(max(min_value, min(max_value, value)))


def _safe_hex(color: Tuple[float, float, float]) -> str:
    """Convert normalized RGB tuple into HEX string."""
    r, g, b = [int(_clamp(channel, 0, 1) * 255) for channel in color]
    return f"#{r:02x}{g:02x}{b:02x}"


@dataclass
class ModelArtifact:
    model_id: str
    processor: Optional[AutoImageProcessor]
    model: Optional[AutoModelForImageClassification]
    loaded: bool
    error: Optional[str] = None


class PlantVisionPipeline:
    """
    Wraps a HuggingFace vision transformer and augments it with
    deterministic heuristics to produce agronomic KPIs.
    """

    def __init__(self):
        candidate_models = [
            os.getenv("PLANT_VISION_MODEL", "").strip() or "nateraw/plant_disease",
            "apple/mobilevit-xx-small",
        ]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.artifact = self._load_first_available(candidate_models)

    def _load_first_available(self, candidates: List[str]) -> ModelArtifact:
        for model_id in candidates:
            try:
                processor = AutoImageProcessor.from_pretrained(model_id)
                model = AutoModelForImageClassification.from_pretrained(model_id)
                model.eval()
                model.to(self.device)
                LOGGER.info("Loaded vision model %s", model_id)
                return ModelArtifact(
                    model_id=model_id,
                    processor=processor,
                    model=model,
                    loaded=True,
                )
            except Exception as exc:  # pragma: no cover - best effort
                LOGGER.warning("Failed to load %s: %s", model_id, exc)
                last_error = str(exc)
        return ModelArtifact(
            model_id=candidates[-1],
            processor=None,
            model=None,
            loaded=False,
            error=last_error if "last_error" in locals() else "unknown",
        )

    def analyze(self, image_path: str, plant_type: Optional[str] = None) -> Dict[str, Any]:
        """Run the full analysis pipeline synchronously."""
        image = Image.open(image_path).convert("RGB")
        metrics = self._extract_color_metrics(image)
        classification = self._classify_image(image)
        return self._compose_response(metrics, classification, plant_type)

    def _classify_image(self, image: Image.Image) -> Dict[str, Any]:
        """Classify the image using the loaded transformer if available."""
        if not self.artifact.loaded or not self.artifact.processor or not self.artifact.model:
            return {
                "label": "unknown",
                "confidence": 0.42,
                "probabilities": [],
                "model_id": self.artifact.model_id,
                "model_loaded": False,
            }

        inputs = self.artifact.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.artifact.model(**inputs)
            logits = outputs.logits
            probabilities = F.softmax(logits, dim=-1)[0]
            confidence, idx = torch.max(probabilities, dim=-1)

        label = self.artifact.model.config.id2label.get(idx.item(), "unknown")
        flat_probs = probabilities.cpu().tolist()
        return {
            "label": label,
            "confidence": float(confidence.item()),
            "probabilities": flat_probs[:5],
            "model_id": self.artifact.model_id,
            "model_loaded": True,
        }

    def _extract_color_metrics(self, image: Image.Image) -> Dict[str, float]:
        """Compute deterministic metrics from pixel statistics."""
        np_image = np.asarray(image).astype("float32") / 255.0
        green_mean = float(np.mean(np_image[:, :, 1]))
        red_mean = float(np.mean(np_image[:, :, 0]))
        blue_mean = float(np.mean(np_image[:, :, 2]))
        brightness = float(np.mean(np_image))
        texture = float(np.std(np_image))
        saturation = float(np.mean(np.max(np_image, axis=2) - np.min(np_image, axis=2)))

        yellow_mask = (
            (np_image[:, :, 0] > 0.65)
            & (np_image[:, :, 1] > 0.65)
            & (np_image[:, :, 2] < 0.45)
        )
        yellow_ratio = float(np.sum(yellow_mask) / yellow_mask.size)

        brown_mask = (
            (np_image[:, :, 0] > np_image[:, :, 1] + 0.05)
            & (np_image[:, :, 2] < 0.4)
        )
        brown_ratio = float(np.sum(brown_mask) / brown_mask.size)

        ndvi_like = (green_mean - red_mean) / (green_mean + red_mean + 1e-5)
        dominant_color = (
            np.mean(np_image[:, :, 0]),
            np.mean(np_image[:, :, 1]),
            np.mean(np_image[:, :, 2]),
        )

        dryness_factor = _clamp((brown_ratio * 1.2) + (1 - green_mean) * 0.4, 0, 1)
        soil_moisture_percent = _clamp(
            (1 - dryness_factor) * 0.85 + (brightness * 0.15),
            0,
            1,
        ) * 100
        water_level_percent = _clamp(
            (green_mean * 0.6) + ((1 - dryness_factor) * 0.4),
            0,
            1,
        ) * 100
        fertilizer_need_percent = _clamp(
            (yellow_ratio * 1.3) + ((1 - green_mean) * 0.4),
            0,
            1,
        ) * 100
        nitrogen_deficiency_probability = _clamp(yellow_ratio * 1.6, 0, 1)
        leaf_color_index = _clamp(((green_mean - red_mean) + 1) / 2, 0, 1) * 100
        plant_health_score = _clamp(
            (green_mean * 0.55)
            + ((1 - dryness_factor) * 0.25)
            + ((1 - fertilizer_need_percent / 100) * 0.2),
            0,
            1,
        ) * 100

        soil_quality_label = self._soil_quality_label(
            soil_moisture_percent, texture, saturation
        )

        return {
            "green_mean": green_mean,
            "red_mean": red_mean,
            "blue_mean": blue_mean,
            "brightness": brightness,
            "texture": texture,
            "saturation": saturation,
            "yellow_ratio": yellow_ratio,
            "brown_ratio": brown_ratio,
            "ndvi_like": float(ndvi_like),
            "dominant_hex": _safe_hex(dominant_color),
            "dryness_factor": float(dryness_factor),
            "soil_moisture_percent": float(round(soil_moisture_percent, 2)),
            "water_level_percent": float(round(water_level_percent, 2)),
            "fertilizer_need_percent": float(round(fertilizer_need_percent, 2)),
            "nitrogen_deficiency_probability": float(
                round(nitrogen_deficiency_probability, 3)
            ),
            "leaf_color_index": float(round(leaf_color_index, 2)),
            "plant_health_score": float(round(plant_health_score, 2)),
            "soil_quality_label": soil_quality_label,
        }

    @staticmethod
    def _soil_quality_label(
        soil_moisture_percent: float, texture: float, saturation: float
    ) -> str:
        if soil_moisture_percent > 70 and texture > 0.1:
            return "clay"
        if soil_moisture_percent < 35 and saturation < 0.2:
            return "sandy"
        if 35 <= soil_moisture_percent <= 70:
            return "loamy"
        return "silty"

    def _compose_response(
        self,
        metrics: Dict[str, float],
        classification: Dict[str, Any],
        plant_type: Optional[str],
    ) -> Dict[str, any]:
        disease_entry = self._build_disease_entry(classification, metrics)
        nutrients = self._build_nutrient_profile(metrics)
        recommendations = self._build_recommendations(metrics, disease_entry)
        explainability = self._build_explainability(metrics, classification)
        growth_stage = self._infer_growth_stage(metrics["plant_health_score"])

        water_needs_liters = float(
            round(max(0.4, (100 - metrics["soil_moisture_percent"]) / 18), 2)
        )

        return {
            "plant_type": plant_type,
            "plant_health_score": metrics["plant_health_score"],
            "water_level_percent": metrics["water_level_percent"],
            "soil_moisture_percent": metrics["soil_moisture_percent"],
            "fertilizer_need_percent": metrics["fertilizer_need_percent"],
            "leaf_color_index": metrics["leaf_color_index"],
            "dryness_factor": metrics["dryness_factor"],
            "nitrogen_deficiency_probability": metrics[
                "nitrogen_deficiency_probability"
            ],
            "water_needs": water_needs_liters,
            "soil_quality": metrics["soil_quality_label"],
            "detected_diseases": disease_entry["items"],
            "diseases": disease_entry["items"],
            "disease_summary": disease_entry["summary"],
            "nutrient_profile": nutrients,
            "fertilizer_deficiency": self._fertilizer_tags(metrics, nutrients),
            "recommendations": recommendations,
            "growth_stage": growth_stage,
            "explainability": explainability,
            "analysis_metadata": {
                "model_id": classification["model_id"],
                "model_loaded": classification["model_loaded"],
                "confidence": classification["confidence"],
                "ndvi_like": metrics["ndvi_like"],
            },
        }

    def _build_disease_entry(
        self, classification: Dict[str, Any], metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        label = classification["label"].replace("_", " ").title()
        confidence = classification["confidence"]
        severity = "low"
        description = "No significant stress detected."

        if "healthy" in label.lower():
            label = "Healthy"
            severity = "none"
            description = "Plant appears healthy with no major disease signatures."
        elif confidence > 0.65 or metrics["fertilizer_need_percent"] > 55:
            severity = "high" if confidence > 0.8 else "moderate"
            description = (
                "Model detected stress patterns consistent with foliar disease."
            )

        visual_cues = []
        if metrics["yellow_ratio"] > 0.15:
            visual_cues.append("yellowing along leaf margins")
        if metrics["brown_ratio"] > 0.08:
            visual_cues.append("brown lesions spreading inward")
        if metrics["dryness_factor"] > 0.6:
            visual_cues.append("general leaf wilting")

        items = [
            {
                "name": label,
                "confidence": round(confidence, 3),
                "severity": severity,
                "description": description,
                "symptoms": visual_cues,
            }
        ]
        return {
            "items": items,
            "summary": {
                "likely_issue": label,
                "confidence": round(confidence, 3),
                "visual_cues": visual_cues,
            },
        }

    def _build_nutrient_profile(self, metrics: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        nitrogen_level = (
            "low" if metrics["nitrogen_deficiency_probability"] > 0.55 else "optimal"
        )
        phosphorus_level = "optimal" if metrics["soil_moisture_percent"] > 40 else "low"
        potassium_level = "adequate" if metrics["leaf_color_index"] > 45 else "low"

        return {
            "nitrogen": {
                "level": nitrogen_level,
                "value": round(
                    1 - metrics["nitrogen_deficiency_probability"], 2
                ),
            },
            "phosphorus": {
                "level": phosphorus_level,
                "value": round(metrics["soil_moisture_percent"] / 100, 2),
            },
            "potassium": {
                "level": potassium_level,
                "value": round(metrics["leaf_color_index"] / 100, 2),
            },
            "magnesium": {
                "level": "optimal" if metrics["brightness"] > 0.35 else "monitor",
                "value": round(metrics["brightness"], 2),
            },
        }

    @staticmethod
    def _fertilizer_tags(
        metrics: Dict[str, float], nutrients: Dict[str, Dict[str, float]]
    ) -> Dict[str, str]:
        tags = {}
        if metrics["fertilizer_need_percent"] > 60:
            tags["nitrogen"] = "low"
        else:
            tags["nitrogen"] = "adequate"

        tags["phosphorus"] = (
            "low" if nutrients["phosphorus"]["value"] < 0.5 else "adequate"
        )
        tags["potassium"] = (
            "adequate" if nutrients["potassium"]["value"] > 0.5 else "low"
        )
        return tags

    def _build_recommendations(
        self, metrics: Dict[str, float], disease_entry: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        recommendations = []
        dryness = metrics["dryness_factor"]
        fertilizer_need = metrics["fertilizer_need_percent"]
        disease = disease_entry["items"][0]

        if dryness > 0.55:
            recommendations.append(
                {
                    "type": "watering",
                    "priority": "high",
                    "title": "Increase irrigation",
                    "description": f"Water stress detected. Target {round(metrics['water_level_percent'], 1)}% water level within 24h.",
                }
            )

        if fertilizer_need > 55:
            recommendations.append(
                {
                    "type": "fertilizer",
                    "priority": "high",
                    "title": "Boost nitrogen availability",
                    "description": "Apply a nitrogen-rich fertilizer (NPK 20-10-10) at 150g per plant.",
                }
            )

        if disease["severity"] in {"moderate", "high"}:
            recommendations.append(
                {
                    "type": "treatment",
                    "priority": "high",
                    "title": f"Treat {disease['name']}",
                    "description": "Use an appropriate fungicide and remove affected foliage.",
                }
            )

        if not recommendations:
            recommendations.append(
                {
                    "type": "care",
                    "priority": "medium",
                    "title": "Maintain monitoring",
                    "description": "Parameters within acceptable range. Continue monitoring every 3 days.",
                }
            )

        return recommendations

    def _build_explainability(
        self, metrics: Dict[str, float], classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        confidence_breakdown = {
            "color": round(_clamp(metrics["leaf_color_index"] / 100), 2),
            "texture": round(_clamp(metrics["texture"] * 2), 2),
            "dryness": round(_clamp(metrics["dryness_factor"]), 2),
            "disease": round(_clamp(classification["confidence"]), 2),
        }

        visual_indicators = []
        if metrics["yellow_ratio"] > 0.12:
            visual_indicators.append("Yellow chlorosis detected across canopy.")
        if metrics["brown_ratio"] > 0.08:
            visual_indicators.append("Necrotic lesions concentrated on edges.")
        if metrics["soil_moisture_percent"] < 40:
            visual_indicators.append("Low soil moisture signature observed.")

        if not visual_indicators:
            visual_indicators.append("Stable pigmentation with minor variance.")

        return {
            "confidenceBreakdown": confidence_breakdown,
            "visualIndicators": visual_indicators,
        }

    @staticmethod
    def _infer_growth_stage(health_score: float) -> Dict[str, Any]:
        if health_score >= 80:
            stage = "mature"
        elif health_score >= 65:
            stage = "flowering"
        elif health_score >= 45:
            stage = "vegetative"
        else:
            stage = "seedling"

        progress = _clamp(health_score / 100, 0, 1)
        return {"stage": stage, "progress": round(progress, 2)}


async def run_pipeline(image_path: str, plant_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience helper that executes the synchronous pipeline without blocking the event loop.
    """
    pipeline = PlantVisionPipeline()
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, pipeline.analyze, image_path, plant_type)

