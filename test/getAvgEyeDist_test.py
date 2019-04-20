# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the wrapper module,
# test that instead of the system installed one.
sys.path = ["../tobii_pro_wrapper"] + sys.path

import tobii_pro_wrapper as wrapper
import math

class getAvgEyeDistTest(unittest.TestCase):

    def testNotInitedEyeTracker(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.tracking = True
        # tobii_helper.eyetracker is None
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgEyeDist()

    def testNoTracking(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        # tobii_helper.tracking is False
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgEyeDist()

    def testNoGazeData(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgEyeDist()

    def testValidGazeData(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (120.0, 90.0, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (122.0, 91.0, 652.0)
        avgResult = tobii_helper._TobiiHelper__getAvgEyeDist()
        self.assertAlmostEqual(651.0, avgResult, delta = 0.001)

    def testGazeDataWithNoLeftEye(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (120.0, 90.0, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        avgResult = tobii_helper._TobiiHelper__getAvgEyeDist()
        self.assertAlmostEqual(650.0, avgResult, delta = 0.001)

    def testGazeDataWithNoRightEye(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (120.0, 90.0, 650.0)
        avgResult = tobii_helper._TobiiHelper__getAvgEyeDist()
        self.assertAlmostEqual(650.0, avgResult, delta = 0.001)

    def testGazeDataWithNanData(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        avgResult = tobii_helper._TobiiHelper__getAvgEyeDist()
        self.assertAlmostEqual(0.0, avgResult, delta = 0.001)

    def testGazeDataNullXY(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (0.0, 0.0, 700.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (0.0, 0.0, 720.0)
        avgResult = tobii_helper._TobiiHelper__getAvgEyeDist()
        self.assertAlmostEqual(710.0, avgResult, delta = 0.001)

    def testGazeDataNullX(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (0.0, 56.0, 700.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (0.0, 60.0, 720.0)
        avgResult = tobii_helper._TobiiHelper__getAvgEyeDist()
        self.assertAlmostEqual(710.0, avgResult, delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests