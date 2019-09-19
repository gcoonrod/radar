#! /usr/bin/env python3

import requests
import json
import time
import os
import traceback
from datetime import datetime
import numpy as np
from typing import Dict, List, Tuple, Any, Union
import sys
from plane import Plane
from dotenv import load_dotenv


def debug_print(message):
    if DEBUG:
        print(message)


try:
    load_dotenv()
except Exception as ex:
    print("Error loading .env file: ", ex)

API_KEY = os.getenv("API_KEY")
DEBUG = True if os.getenv("DEBUG") == "1" else False
in_test = False

try:
    import unicornhathd as u
except ModuleNotFoundError:
    debug_print("No unicorn hat found. Printing to console only.")
    u = 0


def plot(grid: np.ndarray):
    if not u:
        return
    u.clear()
    for x, y in zip(*np.where(grid[:, :, 2] > 0.)):
        u.set_pixel_hsv(x, y, *grid[x, y])
    u.show()


def log(planes: Dict[str, Plane]):
    t = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    data = [" ".join((str(p.lat), str(p.long), str(p.colour))) for p in planes.values()]
    with open("log.txt", "a") as f:
        f.write(t + " - " + " - ".join(data) + "\n")


def make_grid(planes: Dict[str, Plane],
              x_low, x_high, y_low, y_high) -> np.ndarray:
    grid = np.zeros((16, 16, 3), dtype=np.float32)
    for plane in planes.values():
        h, s = plane.colour
        if plane.type == "static":
            x = int(((plane.lat - x_low) / (x_high - x_low)) * -16. + 16)
            y = int(((plane.long - y_low) / (y_high - y_low)) * 16.)
            grid[x, y] = (h, s, .1)
        b = 1.
        if plane.alt is '':
            plane.alt = None
        alt = int(plane.alt) if plane.alt is not None else 100
        for x, y in reversed(plane.track):
            if (x_low < x < x_high
                    and y_low < y < y_high
                    and alt > 50):
                x = int(((x - x_low) / (x_high - x_low)) * -16. + 16)
                y = int(((y - y_low) / (y_high - y_low)) * 16.)
                # get current brightness of pixel to avoid overwriting
                current_b = grid[x, y, 2]
                grid[x, y] = (h, s, max(current_b, b)) if plane.type != "static" else (h, s, 0.1)
            b /= 2.
    return grid


def purge(planes: Dict[str, Plane]) -> Dict[str, Plane]:
    return {reg: plane for reg, plane in planes.items()
            if (time.time() - plane.last_seen < 45.
                or plane.type == "static")}


def display_to_console(current_ac: Dict[str, Plane]) -> None:
    # current_ac is a dict in form {registration: Plane()}
    if DEBUG:
        for p in [p for p in current_ac.values() if p.type != "static"]:
            print("ICAO:", p.icao or "N/A")
            print("Operation ICAO:", p.opicao or "N/A")
            print("From:", p.frm)
            print("To:", p.to)
            print("Type:", p.mdl)  # p.Type)
            print("Operator:", p.op)
            print("Altitude:", p.alt)
            print("Last Info:", round(time.time() - p.last_seen, 2), "seconds ago")
            print()


def track(fixed_points: List[Tuple[float, float]],
          lat_min: float, lat_max: float, long_min: float, long_max: float,
          r: float = 25.):
    """
    :param fixed_points: list of fixed points to display. first item is tracking centre
    :param r: range (km) of tracking, from centre
    :param lat_min: minimum latitude to use for display grid
    :param lat_max: maximum latitude to use for display grid
    :param long_min: minimum longitude to use for display grid
    :param long_max: maximum longitude to use for display grid
    :return: None
    """
    lat, long = x_low + (x_high - x_low) / 2, y_low + (y_high - y_low) / 2
    if DEBUG:
        print("getting data...")
        print(lat, long, r)

    url = "https://adsbexchange.com/api/aircraft/json/lat/{}/lon/{}/dist/{}".format(
        lat, long, r)
    current_ac = {}

    # add fixed point(s)
    for i, (x, y) in enumerate(fixed_points):
        current_ac["fixed" + str(i)] = Plane("fixed" + str(i),
                                             {"lat": x, "long": y,
                                              "kLat": x, "kLong": y,  # for k_filter
                                              "alt": 0, "type": "static"})

    while True:
        try:
            headers = {
                "api-auth": API_KEY,
                "Accept-Encoding": "deflate"
            }
            req = requests.Request('GET', url=url, headers=headers)
            prepared_req = req.prepare()
            # pretty_print_GET(prepared_req)
            session = requests.Session()
            response = session.send(prepared_req)
            assert response.ok
            data = json.loads(response.text)
            debug_print(json.dumps(data, indent=4, sort_keys=True))

            if "ac" in data:
                if data.get("ac") is None:
                    print("No data from search.")
                    time.sleep(2)
                    continue

                aclist = [{k.lower(): v
                           for k, v in ac.items()}
                          for ac in data.get("ac", {})]
            else:
                aclist = []
        except Exception as e:
            print("{}: error.".format(datetime.strftime(datetime.now(), "%H:%M:%S")))
            print(e)
            traceback.print_exc()
            if not in_test:
                time.sleep(2)
                continue
            else:
                break

        for ac in aclist:
            reg = ac.get("reg")
            core_data = Plane.extract_data(ac)
            # debug_print(core_data)
            if reg:
                plane = current_ac.get(reg)
                if plane:
                    plane.update_fields(core_data)
                else:
                    plane = Plane(reg, core_data)
                    current_ac[reg] = plane

        display_to_console(current_ac)
        current_ac = purge(current_ac)
        grid = make_grid(current_ac, lat_min, lat_max, long_min, long_max)
        plot(grid)
        log(current_ac)
        if not in_test:
            time.sleep(5)
        else:
            break


def get_config_data():
    # load config file - should be config.json in project root
    try:
        with open("config.json", "r") as f:
            map_data = json.load(f)

            # check data format - should be float
            assert type(map_data["bottom_left"][0]) == float
            assert type(map_data["bottom_left"][1]) == float
            assert type(map_data["top_right"][0]) == float
            assert type(map_data["top_right"][1]) == float
            r = float(map_data["range"])
            fixed = list(filter(lambda x: type(x[0]) == float and type(x[1]) == float, map_data["fixed_points"]))
            fixed = [tuple(coord) for coord in fixed]
    except FileNotFoundError:
        debug_print("Please configure location and map data in a config.json.")
        sys.exit(1)

    x_low, y_low = map_data["bottom_left"]
    x_high, y_high = map_data["top_right"]

    # check data is valid
    if not (x_low < x_high and y_low < y_high):
        debug_print("invalid coordinates.")
        sys.exit(1)
    return fixed, x_low, x_high, y_low, y_high, r


def pretty_print_GET(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    debug_print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


if __name__ == '__main__':
    fixed, x_low, x_high, y_low, y_high, r = get_config_data()
    track(fixed, x_low, x_high, y_low, y_high, r)
