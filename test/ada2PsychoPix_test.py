# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the calibrator module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as calibrator

class ada2PsychoPixTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def testNoneParam(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__ada2PsychoPix(None)

    def testParamWithWrongType(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__ada2PsychoPix([])

    def testTupleParamWithWrongLen(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__ada2PsychoPix((12, 11, 10))
            
    def testNanTupleParam(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__ada2PsychoPix(("12", "11"))
            
    def testNonNormalParam(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__ada2PsychoPix((2.0, 0.5))           
            
    def testNonInitedMonitor(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__ada2PsychoPix((0.5, 0.5))
            
    def testOriginPoint(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        pixResult = tobii_helper._TobiiHelper__ada2PsychoPix((0.0, 0.0))
        self.assertAlmostEqual(-683, pixResult[0], delta = 0.001)
        self.assertAlmostEqual(384, pixResult[1], delta = 0.001)
        
    def testOnePoint(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        pixResult = tobii_helper._TobiiHelper__ada2PsychoPix((1.0, 1.0))
        self.assertAlmostEqual(683, pixResult[0], delta = 0.001)
        self.assertAlmostEqual(-384, pixResult[1], delta = 0.001)
        
    def testRandomPoint(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        pixResult = tobii_helper._TobiiHelper__ada2PsychoPix((0.234, 0.52))
        self.assertAlmostEqual(-363, pixResult[0], delta = 0.001)
        self.assertAlmostEqual(-15, pixResult[1], delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests