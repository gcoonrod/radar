import os
from unittest import TestCase
from unittest.mock import patch

from requests import Session

from tracker import Tracker

CWD = os.path.dirname(os.path.abspath(__file__))
test_data_path = os.path.join(CWD, 'data.json')


class TestTracker(TestCase):
    json_data = None

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code
            self.ok = True

    def mocked_get(*args, **kwargs):
        return TestTracker.MockResponse(TestTracker.json_data, 200)

    @classmethod
    def setUpClass(cls):
        with open(test_data_path) as json_file:
            cls.json_data = json_file.read()

    @patch.object(Session, 'send', side_effect=mocked_get)
    def test_track(self, mock_get):
        tracker = Tracker({
            "fixed": [],
            "x_low": 0.,
            "x_high": 0.,
            "y_low": 0.,
            "y_high": 0.,
            "r": 0.
        }, 0)
        tracker.in_test = True
        tracker.track()
        pass
