# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the wrapper module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as wrapper
import math

class getAvgGazePosTest(unittest.TestCase):

    def testNotInitedEyeTracker(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.tracking = True
        # tobii_helper.eyetracker is None
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgGazePos()

    def testNoTracking(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        # tobii_helper.tracking is False
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgGazePos()

    def testNoGazeData(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getAvgGazePos()

    def testValidGazeData(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (0.34, 0.56)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (0.32, 0.61)
        avgResult = tobii_helper._TobiiHelper__getAvgGazePos()
        self.assertAlmostEqual(0.33, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(0.585, avgResult[1], delta = 0.001)

    def testGazeDataWithNoLeftEye(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (0.34, 0.56)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (math.nan, math.nan)
        avgResult = tobii_helper._TobiiHelper__getAvgGazePos()
        self.assertAlmostEqual(0.34, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(0.56, avgResult[1], delta = 0.001)

    def testGazeDataWithNoRightEye(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (0.72, 0.46)
        avgResult = tobii_helper._TobiiHelper__getAvgGazePos()
        self.assertAlmostEqual(0.72, avgResult[0], delta = 0.001)
        self.assertAlmostEqual(0.46, avgResult[1], delta = 0.001)

    def testGazeDataWithNanData(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (math.nan, math.nan)
        avgResult = tobii_helper._TobiiHelper__getAvgGazePos()
        self.assertTrue(math.isnan(avgResult[0]))
        self.assertTrue(math.isnan(avgResult[1]))

if __name__ == "__main__":
    unittest.main() # run all tests