import json
import os
from unittest import TestCase

from plane import Plane

CWD = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(CWD, 'data.json')


class TestPlane(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(test_data_path) as json_file:
            data = json.load(json_file)
            cls.aclist = data.get("ac")

    def test_set_colour(self):
        plane_data = self.aclist[0]
        test_plane = Plane(reg=plane_data['reg'], attr=plane_data)
        self.assertIsNotNone(test_plane.colour)
        self.assertEqual(test_plane.colour, (.369, .89), "Plane color is not equal.")

        pass

    def test_extract_data(self):
        raw_plane_data = self.aclist[1]
        extracted_plane_data = Plane.extract_data(raw_plane_data)
        self.assertIsNone(extracted_plane_data.get('altt'))
        pass
