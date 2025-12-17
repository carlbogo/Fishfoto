# backend/pipeline/visualizer.py
import cv2
import numpy as np
from typing import List, Tuple


# BGR colors for OpenCV
COLOR_MAP = {
    "kilu": (0, 200, 0),    # green
    "raim": (0, 0, 255),    # red
    "unknown": (200, 200, 200),
}


def draw_fish_masks(
        image_rgb: np.ndarray,
        masks_with_labels: List[Tuple[np.ndarray, str]],
) -> np.ndarray:
    """
    Draws polygon contours for all masks on the image,
    colored by fish class.
    """

    vis = image_rgb.copy()
    vis_bgr = cv2.cvtColor(vis, cv2.COLOR_RGB2BGR)

    for mask, label in masks_with_labels:
        color = COLOR_MAP.get(label, COLOR_MAP["unknown"])

        mask_uint8 = (mask > 0).astype(np.uint8) * 255
        contours, _ = cv2.findContours(
            mask_uint8,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        cv2.drawContours(
            vis_bgr,
            contours,
            -1,
            color,
            thickness=3,
        )

    return cv2.cvtColor(vis_bgr, cv2.COLOR_BGR2RGB)
