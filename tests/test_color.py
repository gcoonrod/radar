from unittest import TestCase

from color import Color


class TestColor(TestCase):
    def test_convert_hue_to_unit(self):
        # Check outer bounds
        self.assertEqual(0.0, Color.convert_hue_to_unit(0))
        self.assertEqual(1.0, Color.convert_hue_to_unit(360))

        # Check defined colors
        self.assertEqual(Color.convert_hue_to_unit(Color.BLUE.hue), .667)
        self.assertEqual(Color.convert_hue_to_unit(Color.RED.hue), 0.0)
        self.assertEqual(Color.convert_hue_to_unit(Color.GREEN.hue), .319)
        self.assertEqual(Color.convert_hue_to_unit(Color.YELLOW.hue), .167)
        self.assertEqual(Color.convert_hue_to_unit(Color.LIGHT_BLUE.hue), .514)
        self.assertEqual(Color.convert_hue_to_unit(Color.VIOLET.hue), .833)
        pass

    def test_convert_unit_to_hue(self):
        # Check outer bounds
        self.assertEqual(0, Color.convert_unit_to_hue(0))
        self.assertEqual(360, Color.convert_unit_to_hue(1.0))

        # Check defined colors
        self.assertEqual(Color.convert_unit_to_hue(.667), Color.BLUE.hue)
        self.assertEqual(Color.convert_unit_to_hue(0.0), Color.RED.hue)
        self.assertEqual(Color.convert_unit_to_hue(.319), Color.GREEN.hue)
        self.assertEqual(Color.convert_unit_to_hue(.167), Color.YELLOW.hue)
        self.assertEqual(Color.convert_unit_to_hue(.514), Color.LIGHT_BLUE.hue)
        self.assertEqual(Color.convert_unit_to_hue(.833), Color.VIOLET.hue)
        pass
