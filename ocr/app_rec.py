import torch
import os
os.environ["USE_TORCH"] = "1"
import cropper_rec
from typing import List,Tuple
from doctr.models import recognition_predictor,crnn_mobilenet_v3_small


def rec(images: List) -> List[Tuple[str,float]]:
    """Return the values and confidences of Yugioh card IDs after recognition only assuming we know the position of ID.

    Args:
        images (List[np.ndarray]): List of images represented as numpy arrays.

    Returns:
        Tuple(str,float): The value of yugioh card ID with its confidence
    """
    doc=cropper_rec.crop(images)

    rec_model = crnn_mobilenet_v3_small(pretrained=False)

    rec_model.load_state_dict(torch.load("crnn_mobilenet_v3_small_pretranied.pt", map_location="cpu"))

    predictor = recognition_predictor(arch=rec_model)

    res = predictor(doc)

    return res