import cv2
import numpy as np
from typing import List

def draw_fish_masks(
        image_rgb: np.ndarray,
        masks: List[np.ndarray],
) -> np.ndarray:
    """
    Draws contours of fish masks on the image.
    Returns an RGB image.
    """

    vis = image_rgb.copy()
    vis_bgr = cv2.cvtColor(vis, cv2.COLOR_RGB2BGR)

    for mask in masks:
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
            (52, 52, 235),  # red-ish
            thickness=3,
        )

    return cv2.cvtColor(vis_bgr, cv2.COLOR_BGR2RGB)
