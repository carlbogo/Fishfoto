from typing import Optional, Tuple
import numpy as np
import cv2


# Class mappings (keep them explicit)
CLASS_TO_ID = {"kilu": 0, "raim": 1}
ID_TO_CLASS = {0: "kilu", 1: "raim"}


def classify_fish(
        *,
        image_rgb: np.ndarray,
        classification_model,
        conf_thresh: float = 0.25,
) -> Optional[Tuple[str, float]]:
    """
    Classifies a single fish image as 'kilu' or 'raim'.

    Parameters
    ----------
    image_rgb : np.ndarray
        Input image in RGB format (H, W, 3)
    classification_model : YOLO
        Loaded YOLO classification model
    conf_thresh : float
        Minimum confidence threshold

    Returns
    -------
    Optional[Tuple[str, float]]
        (predicted_class, confidence) if above threshold,
        None if confidence too low
    """

    # YOLO expects BGR for NumPy input
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    preds = classification_model.predict(
        source=image_bgr,
        imgsz=640,
        verbose=False,
    )[0]

    # Safety check (should rarely fail)
    if preds.probs is None:
        return None

    probs = preds.probs.data.cpu().numpy()
    pred_id = int(preds.probs.top1)
    pred_conf = float(probs[pred_id])

    if pred_conf < conf_thresh:
        return None

    pred_class = ID_TO_CLASS[pred_id]
    return pred_class, pred_conf
