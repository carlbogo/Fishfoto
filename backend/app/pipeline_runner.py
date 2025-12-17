from pathlib import Path
from io import BytesIO
import base64
import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor

from backend.pipeline.extractor import extract_objects_from_image
from backend.pipeline.classifier import classify_fish
from backend.pipeline.visualizer import draw_fish_masks
from backend.utils import ensure_sam_weights


# -------------------------------------------------
# Paths & device
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

YOLO_EXTRACTOR_WEIGHTS = PROJECT_ROOT / "models/extractor/Yolo/best.pt"
YOLO_CLASSIFIER_WEIGHTS = PROJECT_ROOT / "models/classifier/Yolo/best.pt"
SAM_WEIGHTS = PROJECT_ROOT / "models/extractor/SAM/sam_vit_h_4b8939.pth"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# -------------------------------------------------
# Load models ONCE (import time)
# -------------------------------------------------
ensure_sam_weights(SAM_WEIGHTS)

extraction_model = YOLO(YOLO_EXTRACTOR_WEIGHTS)
classification_model = YOLO(YOLO_CLASSIFIER_WEIGHTS)

sam = sam_model_registry["vit_h"](checkpoint=SAM_WEIGHTS)
sam.to(DEVICE)
sam_predictor = SamPredictor(sam)


# -------------------------------------------------
# Helper: RGB image → base64 PNG
# -------------------------------------------------
def image_rgb_to_base64(image_rgb: np.ndarray) -> str:
    img = Image.fromarray(image_rgb)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


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
    Full pipeline:
    - extract fish (YOLO + SAM)
    - classify each fish
    - count classes
    - visualize detected fish
    """

    extracted = extract_objects_from_image(
        image_rgb=image_rgb,
        extraction_model=extraction_model,
        sam_predictor=sam_predictor,
        min_area=min_area,
    )

    total_fish = 0
    num_kilu = 0
    num_raim = 0

    masks = []

    for fish in extracted:
        crop = fish["crop"]
        mask = fish["mask"]

        pred = classify_fish(
            image_rgb=crop,
            classification_model=classification_model,
            conf_thresh=conf_thresh,
        )

        if pred is None:
            continue

        label, _confidence = pred

        total_fish += 1
        masks.append(mask)

        if label == "kilu":
            num_kilu += 1
        elif label == "raim":
            num_raim += 1

    # Draw contours on original image
    vis_image = draw_fish_masks(
        image_rgb=image_rgb,
        masks=masks,
    )

    vis_base64 = image_rgb_to_base64(vis_image)

    return {
        "total_fish": total_fish,
        "num_kilu": num_kilu,
        "num_raim": num_raim,
        "image_base64": vis_base64,
    }
