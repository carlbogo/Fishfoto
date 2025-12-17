from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

from backend.app.pipeline_runner import process_image

app = FastAPI(title="Fishfoto API")


@app.post("/process")
async def process_endpoint(file: UploadFile = File(...)):
    """
    Upload an image and get fish classifications.
    """

    contents = await file.read()

    image_bgr = cv2.imdecode(
        np.frombuffer(contents, np.uint8),
        cv2.IMREAD_COLOR,
    )

    if image_bgr is None:
        return {"error": "Invalid image"}

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    result = process_image(image_rgb=image_rgb)

    return result
