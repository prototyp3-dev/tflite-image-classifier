from io import BytesIO
from PIL import Image

import numpy as np


class ImageInput:
    """
    Abstraction for an image that will be used as the input for a ML Model
    """

    def __init__(self, img: Image.Image):
        self._img = img

    def get_resized_nparray(self, height: int, width: int) -> np.ndarray:
        resized_img = self._img.resize((width, height))

        if resized_img.mode != 'RGB':
            resized_img = resized_img.convert('RGB')

        final_arr = np.expand_dims(resized_img, axis=0)
        return final_arr


def from_bytes(data: bytes):
    buffer = BytesIO(data)
    pil_img = Image.open(buffer)
    return ImageInput(pil_img)
