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

class trackboxEyePosTest(unittest.TestCase):

    def initTrackBox(self, tobii_helper):
        tobii_helper.tbCoordinates = {}
        tobii_helper.tbCoordinates['bottomLeft'] = (-150.0, -121.0, 500.0)
        tobii_helper.tbCoordinates['bottomRight'] = (150.0, -121.0, 500.0)
        tobii_helper.tbCoordinates['topLeft'] = (-150.0, 121.0, 500.0)
        tobii_helper.tbCoordinates['topRight'] = (150.0, 121.0, 500.0)
        tobii_helper.tbCoordinates['height'] = 2.0 * 121.0
        tobii_helper.tbCoordinates['width'] = 2.0 * 150.0

    def initDisplayArea(self, tobii_helper):
        tobii_helper.adaCoordinates = {}
        tobii_helper.adaCoordinates['bottomLeft'] = (-237.45, 13.21, -10.88)
        tobii_helper.adaCoordinates['bottomRight'] = (239.19, 13.21, -10.88)
        tobii_helper.adaCoordinates['topLeft'] = (-237.45, 259.32, 93.58)
        tobii_helper.adaCoordinates['topRight'] = (239.19, 259.32, 93.58)
        tobii_helper.adaCoordinates['height'] = 267.36
        tobii_helper.adaCoordinates['width'] = 476.64

    def testNotInitedEyeTracker(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.tracking = True
        # tobii_helper.eyetracker is None
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__trackboxEyePos()

    def testNoTracking(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        # tobii_helper.tracking is False
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__trackboxEyePos()

    def testNoGazeData(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__trackboxEyePos()

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
        self.initDisplayArea(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__trackboxEyePos()
        self.assertAlmostEqual(0.171, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(0.192, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, rightPos[1], delta = 0.001)

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
        self.initDisplayArea(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__trackboxEyePos()
        self.assertAlmostEqual(0.171, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(0.99, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(0.99, rightPos[1], delta = 0.001)

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
        self.initDisplayArea(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__trackboxEyePos()
        self.assertAlmostEqual(0.99, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(0.99, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(0.171, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, rightPos[1], delta = 0.001)

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
        self.initDisplayArea(tobii_helper)
        leftPos, rightPos = tobii_helper._TobiiHelper__trackboxEyePos()
        self.assertAlmostEqual(0.99, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(0.99, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(0.99, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(0.99, rightPos[1], delta = 0.001)

    def testRatioOnePointOne(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (1.0, 1.0, 1.0)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (1.0, 1.0, 1.0)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = True
        self.initTrackBox(tobii_helper)
        tobii_helper.adaCoordinates = tobii_helper.tbCoordinates
        leftPos, rightPos = tobii_helper._TobiiHelper__trackboxEyePos()
        self.assertAlmostEqual(-0.85, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(-0.5, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(-0.85, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(-0.5, rightPos[1], delta = 0.001)

    def testRatioOnePointZero(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.0, 0.0, 0.0)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.0, 0.0, 0.0)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = True
        self.initTrackBox(tobii_helper)
        tobii_helper.adaCoordinates = tobii_helper.tbCoordinates
        leftPos, rightPos = tobii_helper._TobiiHelper__trackboxEyePos()
        self.assertAlmostEqual(0.85, leftPos[0], delta = 0.001)
        self.assertAlmostEqual(0.5, leftPos[1], delta = 0.001)
        self.assertAlmostEqual(0.85, rightPos[0], delta = 0.001)
        self.assertAlmostEqual(0.5, rightPos[1], delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests