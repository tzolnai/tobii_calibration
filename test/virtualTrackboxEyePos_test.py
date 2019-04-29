# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the calibrator module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as calibrator
import math

class virtualTrackboxEyePosTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def initTrackBox(self, tobii_helper):
        tobii_helper.tbCoordinates = {}
        tobii_helper.tbCoordinates['bottomLeft'] = (-150.0, -121.0, 500.0)
        tobii_helper.tbCoordinates['bottomRight'] = (150.0, -121.0, 500.0)
        tobii_helper.tbCoordinates['topLeft'] = (-150.0, 121.0, 500.0)
        tobii_helper.tbCoordinates['topRight'] = (150.0, 121.0, 500.0)
        tobii_helper.tbCoordinates['height'] = 2.0 * 121.0
        tobii_helper.tbCoordinates['width'] = 2.0 * 150.0

        tobii_helper.virtual_trackbox_height = 413.215
        tobii_helper.virtual_trackbox_width = 512.25

    def testNotInitedEyeTracker(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.tracking = True
        # tobii_helper.eyetracker is None
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__virtualTrackboxEyePos()

    def testNoTracking(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        # tobii_helper.tracking is False
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__virtualTrackboxEyePos()

    def testNoGazeData(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__virtualTrackboxEyePos()

    def testValidGazeData(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.11)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.12)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = True
        self.initTrackBox(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__virtualTrackboxEyePos()
        self.assertAlmostEqual(81.959, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(92.204, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, rightPos[1], delta = 0.001)

    def testGazeDataWithNoRightEye(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.11)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = False
        self.initTrackBox(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__virtualTrackboxEyePos()
        self.assertAlmostEqual(81.959, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, leftPos[1], delta = 0.001)
        self.assertTrue(math.isnan(rightPos[0]))
        self.assertTrue(math.isnan(rightPos[1]))

    def testGazeDataWithNoLeftEye(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.11)
        tobii_helper.gazeData['left_gaze_origin_validity'] = False
        tobii_helper.gazeData['right_gaze_origin_validity'] = True
        self.initTrackBox(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__virtualTrackboxEyePos()
        self.assertTrue(math.isnan(leftPos[0]))
        self.assertTrue(math.isnan(leftPos[1]))
        self.assertAlmostEqual(81.959, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, rightPos[1], delta = 0.001)

    def testGazeDataWithNoValidEye(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['left_gaze_origin_validity'] = False
        tobii_helper.gazeData['right_gaze_origin_validity'] = False
        self.initTrackBox(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__virtualTrackboxEyePos()
        self.assertTrue(math.isnan(leftPos[0]))
        self.assertTrue(math.isnan(leftPos[1]))
        self.assertTrue(math.isnan(rightPos[0]))
        self.assertTrue(math.isnan(rightPos[1]))

if __name__ == "__main__":
    unittest.main() # run all tests