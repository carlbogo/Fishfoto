from pathlib import Path
import numpy as np
import torch
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor

from backend.pipeline.extractor import extract_objects_from_image
from backend.pipeline.classifier import classify_fish
from backend.utils import ensure_sam_weights


# -------------------------------------------------
# Paths & device
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

YOLO_EXTRACTOR_WEIGHTS = PROJECT_ROOT / "models/yolo/best.pt"
YOLO_CLASSIFIER_WEIGHTS = PROJECT_ROOT / "models/yolo/classifier.pt"
SAM_WEIGHTS = PROJECT_ROOT / "models/extractor/SAM/sam_vit_h_4b8939.pth"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# -------------------------------------------------
# Load models ONCE
# -------------------------------------------------
ensure_sam_weights(SAM_WEIGHTS)

extraction_model = YOLO(YOLO_EXTRACTOR_WEIGHTS)
classification_model = YOLO(YOLO_CLASSIFIER_WEIGHTS)

sam = sam_model_registry["vit_h"](checkpoint=SAM_WEIGHTS)
sam.to(DEVICE)
sam_predictor = SamPredictor(sam)


# -------------------------------------------------
# Public pipeline function
# -------------------------------------------------
def process_image(
        *,
        image_rgb: np.ndarray,
        min_area: int = 10_000,
        conf_thresh: float = 0.25,
) -> dict:
    """
    Full pipeline: extract fish → classify each one
    """

    crops = extract_objects_from_image(
        image_rgb=image_rgb,
        extraction_model=extraction_model,
        sam_predictor=sam_predictor,
        min_area=min_area,
    )

    results = []

    for crop in crops:
        pred = classify_fish(
            image_rgb=crop,
            classification_model=classification_model,
            conf_thresh=conf_thresh,
        )

        label, confidence = pred if pred else (None, None)

        results.append(
            {
                "label": label,
                "confidence": confidence,
            }
        )

    return {
        "num_detected": len(crops),
        "results": results,
    }
