# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the wrapper module,
# test that instead of the system installed one.
sys.path = ["../tobii_pro_wrapper"] + sys.path

import tobii_pro_wrapper as wrapper

class tb2PsychoNormTest(unittest.TestCase):

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

    def testNoneParam(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper.tb2PsychoNorm(None)

    def testParamWithWrongType(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.tb2PsychoNorm([])

    def testTupleParamWithWrongLen(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper.tb2PsychoNorm((12, 11, 10))

    def testNoTrackBoxInited(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper.tb2PsychoNorm((12, 11))

    def testNoDisplayAreAInited(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        with self.assertRaises(ValueError):
            tobii_helper.tb2PsychoNorm((12, 11))

    def testNoneNormalizedParam(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        self.initDisplayArea(tobii_helper)
        with self.assertRaises(ValueError):
            adaResult = tobii_helper.tb2PsychoNorm((12, 11))

    def testNormalizedCall(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        self.initDisplayArea(tobii_helper)
        adaResult = tobii_helper.tb2PsychoNorm((0.34, 0.45))
        self.assertAlmostEqual(-0.100, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(0.045, adaResult[1], delta = 0.001)

    def testRatioOne(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        tobii_helper.adaCoordinates = tobii_helper.tbCoordinates
        adaResult = tobii_helper.tb2PsychoNorm((0.34, 0.45))
        self.assertAlmostEqual(-0.159, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(0.049, adaResult[1], delta = 0.001)

    def testCallWithPointOne(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        self.initDisplayArea(tobii_helper)
        adaResult = tobii_helper.tb2PsychoNorm((1.0, 1.0))
        self.assertAlmostEqual(0.314, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(-0.452, adaResult[1], delta = 0.001)

    def testCallWithPointZero(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        self.initDisplayArea(tobii_helper)
        adaResult = tobii_helper.tb2PsychoNorm((0.0, 0.0))
        self.assertAlmostEqual(-0.314, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(0.452, adaResult[1], delta = 0.001)

    def testRatioOnePointOne(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        tobii_helper.adaCoordinates = tobii_helper.tbCoordinates
        adaResult = tobii_helper.tb2PsychoNorm((1.0, 1.0))
        self.assertAlmostEqual(0.5, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(-0.5, adaResult[1], delta = 0.001)

    def testRatioOnePointZero(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        tobii_helper.adaCoordinates = tobii_helper.tbCoordinates
        adaResult = tobii_helper.tb2PsychoNorm((0.0, 0.0))
        self.assertAlmostEqual(-0.5, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(0.5, adaResult[1], delta = 0.001)

    def testRatioOnePointCenter(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initTrackBox(tobii_helper)
        tobii_helper.adaCoordinates = tobii_helper.tbCoordinates
        adaResult = tobii_helper.tb2PsychoNorm((0.5, 0.5))
        self.assertAlmostEqual(0.0, adaResult[0], delta = 0.001)
        self.assertAlmostEqual(0.0, adaResult[1], delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests