# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the calibrator module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as calibrator

class trackBox2VirtualTrackBoxTest(unittest.TestCase):

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

    def testNoneParam(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__trackBox2VirtualTrackBox(None)

    def testParamWithWrongType(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__trackBox2VirtualTrackBox([])

    def testTupleParamWithWrongLen(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__trackBox2VirtualTrackBox((12, 11, 10))

    def testNoTrackBoxInited(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__trackBox2VirtualTrackBox((12, 11))

    def testNormalCall(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initTrackBox(tobii_helper)
        result = tobii_helper._TobiiHelper__trackBox2VirtualTrackBox((0.34, 0.45))
        self.assertAlmostEqual(81.959, result[0], delta = 0.001)
        self.assertAlmostEqual(20.660, result[1], delta = 0.001)

    def testCallWithPointOne(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initTrackBox(tobii_helper)
        result = tobii_helper._TobiiHelper__trackBox2VirtualTrackBox((1.0, 1.0))
        self.assertAlmostEqual(-256.125, result[0], delta = 0.001)
        self.assertAlmostEqual(-206.607, result[1], delta = 0.001)

    def testCallWithPointZero(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initTrackBox(tobii_helper)
        result = tobii_helper._TobiiHelper__trackBox2VirtualTrackBox((0.0, 0.0))
        self.assertAlmostEqual(256.125, result[0], delta = 0.001)
        self.assertAlmostEqual(206.607, result[1], delta = 0.001)

    def testPointCenter(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initTrackBox(tobii_helper)
        result = tobii_helper._TobiiHelper__trackBox2VirtualTrackBox((0.5, 0.5))
        self.assertAlmostEqual(0.0, result[0], delta = 0.001)
        self.assertAlmostEqual(0.0, result[1], delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests