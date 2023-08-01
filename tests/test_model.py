from pathlib import Path
import unittest

from dapp import images, model

class TestModel(unittest.TestCase):

    def setUp(self) -> None:
        img_path = Path(__file__).with_name('grace_hopper.jpg')
        img_bytes = img_path.read_bytes()
        self.img = images.from_bytes(img_bytes)
        return super().setUp()


    def test_should_return_metadata(self) -> None:

        mdl = model.Model()
        mdl.load()

        meta = mdl.get_metadata()
        self.assertIn('name', meta)
        self.assertIn('version', meta)

    def test_should_predict_image(self) -> None:
        """
        Prediction should be a list of tuples in the format (class, prob)
        """

        mdl = model.Model()
        mdl.load()
        pred = mdl.predict(self.img)

        self.assertIsInstance(pred, list)
        self.assertGreater(len(pred), 0)
        self.assertIsInstance(pred[0][0], str)
        self.assertIsInstance(pred[0][1], float)
        self.assertEqual(pred[0][0], '653:military uniform')
