# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import sys
# Add the local path of the calibrator module,
# use that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as tc
import tobii_research as tobii

import time
from pynput import mouse

gaze_data_callback = None

class EyeTrackerMock:
    def subscribe_to(self, subscription_type, callback, as_dictionary=False):
        gazeData = {}
        gazeData['left_gaze_point_on_display_area'] = (0.5, 0.5)
        gazeData['right_gaze_point_on_display_area'] = (0.5, 0.5)
        callback(gazeData)
        global gaze_data_callback
        gaze_data_callback = callback

    def unsubscribe_from(self, subscription_type, callback=None):
        pass

    def get_display_area(self):
        display_area_dict = {}
        display_area_dict['top_left'] = (-237.45, 259.32, 93.58)
        display_area_dict['top_right'] = (239.19, 259.32, 93.58)
        display_area_dict['bottom_right'] = (239.19, 13.21, -10.88)
        display_area_dict['bottom_left'] = (-237.45, 13.21, -10.88)
        display_area_dict['width'] = 267.36
        display_area_dict['height'] = 476.64
        return tobii.DisplayArea(display_area_dict)

    def get_track_box(self):
        track_box_dict = {}
        track_box_dict['front_lower_left'] = (-150.0, -121.0, 500.0)
        track_box_dict['front_lower_right'] = (150.0, -121.0, 500.0)
        track_box_dict['front_upper_left'] = (-150.0, 121.0, 500.0)
        track_box_dict['front_upper_right'] = (150.0, 121.0, 500.0)
        track_box_dict['back_lower_left'] = (-150.0, -121.0, 800.0)
        track_box_dict['back_lower_right'] = (150.0, -121.0, 800.0)
        track_box_dict['back_upper_left'] = (-150.0, 121.0, 800.0)
        track_box_dict['back_upper_right'] = (150.0, 121.0, 800.0)
        return tobii.TrackBox(track_box_dict)


def on_move(x, y):
    xCoord = (x / 1366)
    yCoord = (y / 768)
    gazeData = {}
    gazeData['left_gaze_point_on_display_area'] = (xCoord + 0.1, yCoord)
    gazeData['right_gaze_point_on_display_area'] = (xCoord - 0.1, yCoord)
    gaze_data_callback(gazeData)

tobii_helper = tc.TobiiHelper()
tobii_helper.setMonitor()
#tobii_helper.setEyeTracker()
tobii_helper.eyetracker = EyeTrackerMock()
tobii_helper._TobiiHelper__getTrackerSpace()

with mouse.Listener(on_move=on_move) as listener:
    tobii_helper.runValidation()



