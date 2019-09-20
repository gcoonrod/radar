from collections import namedtuple
from decimal import *

HSV = namedtuple("hsv", "hue saturation value")


class Color:
    WHITE = HSV(0, 0.0, 1.0)
    BLACK = HSV(0, 0.0, 0.0)
    BLUE = HSV(240, 1.0, 1.0)
    RED = HSV(0, 1.0, 1.0)
    YELLOW = HSV(60, 1.0, 1.0)
    GREEN = HSV(115, 1.0, 1.0)
    LIGHT_BLUE = HSV(185, 1.0, 1.0)
    VIOLET = HSV(300, 1.0, 1.0)

    @staticmethod
    def convert_hue_to_unit(hue: int) -> float:
        # Set bounds for conversion
        old_max = Decimal(360)
        old_min = Decimal(0)
        new_min = Decimal(0)
        new_max = Decimal(1)

        return float(Color._convert_range_to_range(old_max, old_min, new_max, new_min, Decimal(hue), 3))

    @staticmethod
    def convert_unit_to_hue(unit: float) -> int:
        old_max = Decimal(1)
        old_min = Decimal(0)
        new_min = Decimal(0)
        new_max = Decimal(360)

        return int(Color._convert_range_to_range(old_max, old_min, new_max, new_min, Decimal(unit), 3))

    @staticmethod
    def _convert_range_to_range(old_max, old_min, new_max, new_min, old_value, precision):
        getcontext().prec = precision
        old_range = (old_max - old_min)
        if old_range == 0:
            new_value = new_min
        else:
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) / old_range) + new_min

        return new_value
