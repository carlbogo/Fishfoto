from typing import List
import numpy as np
import cv2


# -------------------------------------------------
# Helper: rotate image if vertical
# -------------------------------------------------
def rotate_if_vertical(img_rgb: np.ndarray) -> np.ndarray:
    h, w = img_rgb.shape[:2]
    if h > w:
        return cv2.rotate(img_rgb, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img_rgb


# -------------------------------------------------
# Helper: YOLO prediction, no temp file needed
# -------------------------------------------------
def yolo_predict_rotated(extraction_model, image_rgb: np.ndarray):
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    preds = extraction_model.predict(
        source=image_bgr,
        imgsz=1024,
        conf=0.25,
        verbose=False,
    )[0]

    return preds


# -------------------------------------------------
# Helper: apply mask and return cropped RGB image
# -------------------------------------------------
def masked_crop_from_array(
        image_rgb: np.ndarray,
        mask: np.ndarray,
) -> np.ndarray | None:
    """
        Applies a binary mask to an image and returns the cropped result
        with a white background. Returns None if mask is empty.
    """

    ys, xs = np.where(mask)
    if len(ys) == 0:
        return None

    y0, y1 = ys.min(), ys.max()
    x0, x1 = xs.min(), xs.max()

    crop = image_rgb[y0 : y1 + 1, x0 : x1 + 1]
    m = mask[y0 : y1 + 1, x0 : x1 + 1]

    result = np.full_like(crop, 255)
    result[m] = crop[m]

    return result


# -------------------------------------------------
# MAIN EXTRACTION FUNCTION
# -------------------------------------------------
def extract_objects_from_image(
        *,
        image_rgb: np.ndarray,
        extraction_model,
        sam_predictor,
        min_area: int = 10_000,
) -> List[np.ndarray]:
    """
    Runs YOLO + SAM on a single RGB image and returns extracted object crops.

    Parameters
    ----------
    image_rgb : np.ndarray
        Input image in RGB format (H, W, 3)
    extraction_model : YOLO
        YOLO detection model
    sam_predictor : SamPredictor
        Initialized SAM predictor
    min_area : int
        Minimum mask area threshold

    Returns
    -------
    List[np.ndarray]
        List of extracted RGB images
    """

    extracted_images: List[np.ndarray] = []

    processed_rgb = rotate_if_vertical(image_rgb)
    h, w = processed_rgb.shape[:2]

    # YOLO detection
    preds = yolo_predict_rotated(extraction_model, processed_rgb)

    if preds.boxes is None or len(preds.boxes) == 0:
        return []

    # SAM segmentation
    sam_predictor.set_image(processed_rgb)

    for (x1, y1, x2, y2) in preds.boxes.xyxy.cpu().numpy():

        # Convert YOLO boxes directly to ints
        x1_o, y1_o, x2_o, y2_o = map(int, (x1, y1, x2, y2))

        # Clip to image bounds (still important)
        x1_o = max(0, min(w - 1, x1_o))
        y1_o = max(0, min(h - 1, y1_o))
        x2_o = max(0, min(w - 1, x2_o))
        y2_o = max(0, min(h - 1, y2_o))

        cx_o = (x1_o + x2_o) // 2
        cy_o = (y1_o + y2_o) // 2

        masks, _, _ = sam_predictor.predict(
            point_coords=np.array([[cx_o, cy_o]]),
            point_labels=np.array([1]),
            box=np.array([x1_o, y1_o, x2_o, y2_o]),
            multimask_output=False,
        )

        mask = masks[0]
        if mask.sum() < min_area:
            continue

        crop = masked_crop_from_array(processed_rgb, mask)
        if crop is not None:
            extracted_images.append(crop)

    return extracted_images
