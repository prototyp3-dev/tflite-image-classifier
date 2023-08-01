""""
Test Cases for dapp.images module
"""
import base64
import unittest

import numpy as np

from dapp import images


class TestImages(unittest.TestCase):

    def test_should_read_png_rgb_8bit(self):
        img_encoded = (
            "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAC0lEQVQI12NgQAYAAA"
            "4AATHp3RUAAAAASUVORK5CYII="
        )

        img_bytes = base64.b64decode(img_encoded)

        img = images.from_bytes(img_bytes)
        self.assertIsInstance(img, images.ImageInput)

        arr = img.get_resized_nparray(250, 224)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (1, 250, 224, 3))

    def test_should_read_png_rgba_8bit(self):
        img_encoded = (
            "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAFElEQVQI12NkYGD4z8"
            "DAwMDEAAUADigBA29NMG0AAAAASUVORK5CYII="
        )
        img = base64.b64decode(img_encoded)
        img_bytes = base64.b64decode(img_encoded)

        img = images.from_bytes(img_bytes)
        self.assertIsInstance(img, images.ImageInput)

        arr = img.get_resized_nparray(250, 224)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (1, 250, 224, 3))

    def test_should_read_jpeg(self):
        img_encoded = (
            "/9j/4AAQSkZJRgABAQEBLAEsAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBw"
            "YIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUE"
            "BQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
            "QUFBQUFBQUFBT/wgARCAACAAIDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAA"
            "CP/EABQBAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhADEAAAAVSf/8QAFBABAAAAAA"
            "AAAAAAAAAAAAAAAP/aAAgBAQABBQJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgB"
            "AwEBPwF//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPwF//8QAFBABAAAAAA"
            "AAAAAAAAAAAAAAAP/aAAgBAQAGPwJ//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgB"
            "AQABPyF//9oADAMBAAIAAwAAABCf/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAw"
            "EBPxB//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPxB//8QAFBABAAAAAAAA"
            "AAAAAAAAAAAAAP/aAAgBAQABPxB//9k="
        )

        img = base64.b64decode(img_encoded)
        img_bytes = base64.b64decode(img_encoded)

        img = images.from_bytes(img_bytes)
        self.assertIsInstance(img, images.ImageInput)

        arr = img.get_resized_nparray(250, 224)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (1, 250, 224, 3))
