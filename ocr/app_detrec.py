import os
import torch
os.environ["USE_TORCH"] = "1"
import cropper
import sys
from typing import List,Tuple
from doctr.models import ocr_predictor, sar_resnet31,crnn_mobilenet_v3_small,db_resnet50


rec_model = crnn_mobilenet_v3_small(pretrained=False)
det_model=db_resnet50(pretrained=False)
rec_model.load_state_dict(torch.load("crnn_mobilenet_v3_small_pretranied.pt", map_location="cpu"))
det_model.load_state_dict(torch.load("db_resnet50_latest.pt", map_location="cpu"))
predictor = ocr_predictor(reco_arch=rec_model, 
                          det_arch=det_model,
                          pretrained_backbone=True,
                          assume_straight_pages=True,
                          preserve_aspect_ratio=True,
                          symmetric_pad=True)

def detrec(images: List) -> List[Tuple[str, float]]:
    """Return the values and confidences of Yugioh card IDs after Detection and recognition.

    Args:
        images (List[np.ndarray]): List of images represented as numpy arrays.

    Returns:
        Tuple(str,float): The value of yugioh card ID with its confidence
    """
    doc=cropper.crop(images)
    res = predictor(doc)
    json_resp=res.export()
    answers=[]
    for i in json_resp['pages']:
        resp=i['blocks'][0]['lines'][0]['words'][0]
        value=resp['value']
        confidence=resp['confidence']
        answers.append((value,confidence))
    return answers

