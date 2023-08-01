import pathlib

import numpy as np
from tflite_runtime.interpreter import Interpreter

from . import images


class Model:

    model_name = 'mobilenet_v1'
    model_version = '1.0-224'

    model_file = 'models/mobilenet_v1_1.0_224.tflite'
    labels_file = 'models/labels.txt'

    def __init__(self):
        self.interp: Interpreter | None = None
        self.labels: list[str] | None = None

        self._width: int | None = None
        self._height: int | None = None

        self._is_float: bool | None = None
        self._input_mean: float = 127.5
        self._input_std: float = 127.5
        self._input_idx: int = 0
        self._output_idx: int = 0

    def _get_full_paths(self):
        project_root = pathlib.Path(__file__).parent.parent
        model_path = (project_root / self.model_file).resolve()
        labels_path = (project_root / self.labels_file).resolve()
        return model_path, labels_path

    def load(self) -> None:
        if self.interp is not None:
            return

        model_path, labels_path = self._get_full_paths()

        self.interp = Interpreter(str(model_path))
        self.interp.allocate_tensors()

        with labels_path.open() as fin:
            self.labels = [x.strip() for x in fin]

        input_details = self.interp.get_input_details()
        self._height = input_details[0]['shape'][1]
        self._width = input_details[0]['shape'][2]
        self._is_float = input_details[0]['dtype'] == np.float32
        self._input_idx = input_details[0]['index']

        output_details = self.interp.get_output_details()
        self._output_idx = output_details[0]['index']

    def get_metadata(self) -> dict:
        return {
            'name': self.model_name,
            'version': self.model_version,
        }

    def predict(self, X: images.ImageInput):

        # Preprocess input
        img_data = X.get_resized_nparray(width=self._width, height=self._height)

        if self._is_float:
            img_data = (
                (img_data.astype('float32') - self._input_mean)
                / self._input_std
            )

        # Invoke Inference
        self.interp.set_tensor(self._input_idx, img_data)
        self.interp.invoke()
        output = self.interp.get_tensor(self._output_idx)
        output = output.squeeze()

        # Format Output
        top_k = output.argsort()[-5:][::-1]
        results = []

        for idx in top_k:
            results.append((self.labels[idx], float(output[idx])))

        return results
