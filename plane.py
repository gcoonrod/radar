import time
from collections import deque
from typing import Dict

import numpy as np

from color import Color
from planes import *


# from kalman import KalmanFilter

def tuple_from_type(plane: PlaneType) -> tuple:
    unit = Color.convert_hue_to_unit(plane.hsv.hue)
    return unit, plane.hsv.saturation


class Plane(object):

    def __init__(self, reg: str, attr: Dict):
        self.colour = tuple_from_type(DEFAULT)
        self.reg = reg
        # replace "from" key with "frm"
        attr = {(k if not k == "from" else "frm"): v
                for k, v in attr.items()}
        self.mil = "0"
        self.icao = "N/A"
        self.opicao = "N/A"
        self.__dict__.update(attr)
        self.last_seen = time.time()
        self.set_colour()
        self.reported_track = deque([], maxlen=3)  # used to calculate position
        self.track = deque([], maxlen=3)  # used to store track
        # self.kalman_filter = KalmanFilter(1e-4, .04**2) # measured .04 stddev

    def set_colour(self):
        # Colour is a Tuple with Hue and Saturation (h, s)
        # Both values are between 0 and 1.
        if not self.type:
            self.colour = tuple_from_type(DEFAULT)
            return
        if self.type == "static" or self.mil == "1":
            self.colour = tuple_from_type(STATIC)
        elif self.type.startswith("A38"):
            self.colour = tuple_from_type(A38)
        elif self.type.startswith("B74"):
            self.colour = tuple_from_type(B74)
        elif self.type.startswith("B77"):
            self.colour = tuple_from_type(B77)
        elif self.type.startswith("B78"):
            self.colour = tuple_from_type(B78)
        elif self.type.startswith("B73"):
            self.colour = tuple_from_type(B73)
        elif self.type.startswith("A32") or self.type.startswith("A31"):
            self.colour = tuple_from_type(A32)
        elif self.type.startswith("A33"):
            self.colour = tuple_from_type(A33)
        elif self.type.startswith("A34"):
            self.colour = tuple_from_type(A34)
        else:
            pass

    def update_fields(self, ac: Dict):
        ac = {k: v for k, v in ac.items() if v is not None}
        self.__dict__.update(ac)
        # self.apply_k_filter()
        self.reported_track.append((float(self.lat), float(self.long)))
        self.lat = np.mean([coord[0] for coord in self.reported_track])
        self.long = np.mean([coord[1] for coord in self.reported_track])
        self.track.append((self.lat, self.long))
        self.last_seen = time.time()

    def apply_k_filter(self):
        self.kalman_filter.input_measurement((self.Lat, self.Long))
        self.kLat, self.kLong = self.kalman_filter.get_estimated_position()

    @staticmethod
    def extract_data(ac: Dict) -> Dict:
        keys = ("lat", "lon", "from", "to", "type", "alt", "mdl", "op", "mil", "icao", "opicao")
        data = {k: ac.get(k) for k in keys}
        # data["kLat"], data["kLong"] = ac.get("Lat"), ac.get("Long")

        if "lon" in ac.keys():
            data["long"] = ac.get("lon")

        if "long" in ac.keys():
            data["long"] = ac.get("long")

        return data
