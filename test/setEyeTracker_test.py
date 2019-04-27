# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the calibrator module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as calibrator
import tobii_research as tobii
import time

class setEyeTrackerTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def hasEyeTrackerConnected(self):
        loop_count = 1
        eye_trackers = tobii.find_all_eyetrackers()
        while not eye_trackers and loop_count < 10:
            eye_trackers = tobii.find_all_eyetrackers()
            time.sleep(0.01)
            loop_count += 1
        return loop_count < 10

    def testNoParam(self):
        tobii_helper = calibrator.TobiiHelper()
        if self.hasEyeTrackerConnected():
            tobii_helper.setEyeTracker()
        else:
            with self.assertRaises(ValueError):
                tobii_helper.setEyeTracker()

    def testWrongSerialParam(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.setEyeTracker(serialString = [])

    def testWrongSerialParam2(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper.setEyeTracker(serialString = "12345")

    def testWrongEyeTrackerParam(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.setEyeTracker(eyeTracker = [])

    def testRightSerialNumberParam(self):
        tobii_helper = calibrator.TobiiHelper()
        if self.hasEyeTrackerConnected():
            tobii_helper.setEyeTracker(tobii.find_all_eyetrackers()[0].serial_number)


if __name__ == "__main__":
    unittest.main() # run all tests