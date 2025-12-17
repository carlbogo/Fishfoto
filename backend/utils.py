from pathlib import Path
import urllib.request

SAM_URL = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"


def ensure_sam_weights(path: Path) -> None:
    """
    Ensure that SAM weights exist locally.
    Downloads them once if missing.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return

    print("SAM weights not found.")
    print("Downloading SAM ViT-H weights (~2.4GB). This may take a while...")

    urllib.request.urlretrieve(SAM_URL, path)

    print("SAM weights downloaded.")
