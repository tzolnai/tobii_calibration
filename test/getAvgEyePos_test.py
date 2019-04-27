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

class getAvgEyePosTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def testNotInitedEyeTracker(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.tracking = True
        # tobii_helper.eyetracker is None
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgEyePos()

    def testNoTracking(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        # tobii_helper.tracking is False
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgEyePos()

    def testNoGazeData(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgEyePos()

    def testValidGazeData(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (120.0, 90.0, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (122.0, 91.0, 652.0)
        avgResult = tobii_helper._TobiiHelper__getAvgEyePos()
        self.assertAlmostEqual(121.0, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(90.5, avgResult[1], delta = 0.001)
        self.assertAlmostEqual(651.0, avgResult[2], delta = 0.001)

    def testGazeDataWithNoLeftEye(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (120.0, 90.0, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        avgResult = tobii_helper._TobiiHelper__getAvgEyePos()
        self.assertAlmostEqual(120.0, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(90.0, avgResult[1], delta = 0.001)
        self.assertAlmostEqual(650.0, avgResult[2], delta = 0.001)

    def testGazeDataWithNoRightEye(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (120.0, 90.0, 650.0)
        avgResult = tobii_helper._TobiiHelper__getAvgEyePos()
        self.assertAlmostEqual(120.0, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(90.0, avgResult[1], delta = 0.001)
        self.assertAlmostEqual(650.0, avgResult[2], delta = 0.001)

    def testGazeDataWithNanData(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        avgResult = tobii_helper._TobiiHelper__getAvgEyePos()
        self.assertAlmostEqual(0.0, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(0.0, avgResult[1], delta = 0.001)
        self.assertAlmostEqual(0.0, avgResult[2], delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests