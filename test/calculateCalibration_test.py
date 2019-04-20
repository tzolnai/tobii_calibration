# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the wrapper module,
# test that instead of the system installed one.
sys.path = ["../tobii_pro_wrapper"] + sys.path

import tobii_pro_wrapper as wrapper
import tobii_research as tobii
import math

class myCalibrationResult:
   def __init__(self, status_, calibration_points_):
        self.status = status_
        self.calibration_points = calibration_points_

class calculateCalibrationTest(unittest.TestCase):

    def initCalibPoints(self):
        calibration_point0 = tobii.CalibrationPoint((0.0, 0.0),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.0, 0.0), True),
                                                            tobii.CalibrationEyeData((0.0, 0.0), True)),))
        calibration_point = tobii.CalibrationPoint((0.1, 0.1),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.08, 0.08), True),
                                                            tobii.CalibrationEyeData((0.09, 0.08), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.12, 0.11), True),
                                                            tobii.CalibrationEyeData((0.18, 0.12), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.11, 0.12), True),
                                                            tobii.CalibrationEyeData((0.10, 0.10), True))))
        calibration_point2 = tobii.CalibrationPoint((0.9, 0.9),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.98, 0.98), True),
                                                            tobii.CalibrationEyeData((0.99, 0.98), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.91, 0.90), True),
                                                            tobii.CalibrationEyeData((0.90, 0.97), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.89, 0.87), True),
                                                            tobii.CalibrationEyeData((0.98, 0.99), True))))
        calibration_points = (calibration_point0, calibration_point, calibration_point2)
        return tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)

    def testWrongParam(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__calculateCalibration(None)
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__calculateCalibration([])            

    def testTwoCalibPoints(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor()
        calibResult = self.initCalibPoints()
        calibData = tobii_helper._TobiiHelper__calculateCalibration(calibResult)
        self.assertEqual(2, len(calibData))
        self.assertEqual(4, len(calibData[0]))
        self.assertEqual(4, len(calibData[1]))

        # (0.1,0.1)
        # average sample point
        self.assertEqual(-546, calibData[0][0][0])
        self.assertEqual(307, calibData[0][0][1])
        # average left eye sample point
        self.assertEqual(-541, calibData[0][1][0])
        self.assertEqual(304, calibData[0][1][1])
        # average right eye sample point
        self.assertEqual(-514, calibData[0][2][0])
        self.assertEqual(307, calibData[0][2][1])

        # (0.9,0.9)
        # average sample point
        self.assertEqual(546, calibData[1][0][0])
        self.assertEqual(-307, calibData[1][0][1])
        # average left eye sample point
        self.assertEqual(582, calibData[1][1][0])
        self.assertEqual(-320, calibData[1][1][1])
        # average right eye sample point
        self.assertEqual(623, calibData[1][2][0])
        self.assertEqual(-368, calibData[1][2][1])
        
    def testTwoCalibPointsOneSample(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor()

        calibration_point0 = tobii.CalibrationPoint((0.0, 0.0),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.0, 0.0), True),
                                                            tobii.CalibrationEyeData((0.0, 0.0), True)),))
        calibration_point = tobii.CalibrationPoint((0.1, 0.1),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.08, 0.08), True),
                                                            tobii.CalibrationEyeData((0.09, 0.08), True)),))
        calibration_point2 = tobii.CalibrationPoint((0.9, 0.9),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.98, 0.98), True),
                                                            tobii.CalibrationEyeData((0.99, 0.98), True)),))

        calibration_points = (calibration_point0, calibration_point, calibration_point2)
        calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)        
        calibData = tobii_helper._TobiiHelper__calculateCalibration(calibResult)
        self.assertEqual(2, len(calibData))
        self.assertEqual(4, len(calibData[0]))
        self.assertEqual(4, len(calibData[1]))

        # (0.1,0.1)
        # average sample point
        self.assertEqual(-546, calibData[0][0][0])
        self.assertEqual(307, calibData[0][0][1])
        # average left eye sample point
        self.assertEqual(-573, calibData[0][1][0])
        self.assertEqual(322, calibData[0][1][1])
        # average right eye sample point
        self.assertEqual(-560, calibData[0][2][0])
        self.assertEqual(322, calibData[0][2][1])

        # (0.9,0.9)
        # average sample point
        self.assertEqual(546, calibData[1][0][0])
        self.assertEqual(-307, calibData[1][0][1])
        # average left eye sample point
        self.assertEqual(655, calibData[1][1][0])
        self.assertEqual(-368, calibData[1][1][1])
        # average right eye sample point
        self.assertEqual(669, calibData[1][2][0])
        self.assertEqual(-368, calibData[1][2][1])
        
    def testNanSamplePoints(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor()

        calibration_point0 = tobii.CalibrationPoint((0.0, 0.0),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.0, 0.0), True),
                                                            tobii.CalibrationEyeData((0.0, 0.0), True)),))
        calibration_point = tobii.CalibrationPoint((0.1, 0.1),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((math.nan, math.nan), True),
                                                            tobii.CalibrationEyeData((math.nan, math.nan), True)),))
        calibration_point2 = tobii.CalibrationPoint((0.9, 0.9),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.98, 0.98), True),
                                                            tobii.CalibrationEyeData((0.99, 0.98), True)),))

        calibration_points = (calibration_point0, calibration_point, calibration_point2)
        calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)
        with self.assertRaises(ValueError):        
            calibData = tobii_helper._TobiiHelper__calculateCalibration(calibResult)

    def testOneCalibPoint(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor()
        
        calibration_point0 = tobii.CalibrationPoint((0.0, 0.0),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.0, 0.0), True),
                                                            tobii.CalibrationEyeData((0.0, 0.0), True)),))
        calibration_point = tobii.CalibrationPoint((0.1, 0.1),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.08, 0.08), True),
                                                            tobii.CalibrationEyeData((0.09, 0.08), True)),))
        calibration_points = (calibration_point0, calibration_point)
        calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)                                                               
        calibData = tobii_helper._TobiiHelper__calculateCalibration(calibResult)
        self.assertEqual(1, len(calibData))
        self.assertEqual(4, len(calibData[0]))

        # (0.1,0.1)
        # average sample point
        self.assertEqual(-546, calibData[0][0][0])
        self.assertEqual(307, calibData[0][0][1])
        # average left eye sample point
        self.assertEqual(-573, calibData[0][1][0])
        self.assertEqual(322, calibData[0][1][1])
        # average right eye sample point
        self.assertEqual(-560, calibData[0][2][0])
        self.assertEqual(322, calibData[0][2][1])

    def testFiveCalibPoints(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor()
        
        calibration_point0 = tobii.CalibrationPoint((0.0, 0.0),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.0, 0.0), True),
                                                            tobii.CalibrationEyeData((0.0, 0.0), True)),))
        calibration_point = tobii.CalibrationPoint((0.1, 0.1),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.08, 0.08), True),
                                                            tobii.CalibrationEyeData((0.09, 0.08), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.12, 0.11), True),
                                                            tobii.CalibrationEyeData((0.18, 0.12), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.11, 0.12), True),
                                                            tobii.CalibrationEyeData((0.10, 0.10), True))))
        calibration_point2 = tobii.CalibrationPoint((0.9, 0.1),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.98, 0.08), True),
                                                            tobii.CalibrationEyeData((0.99, 0.09), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.91, 0.12), True),
                                                            tobii.CalibrationEyeData((0.90, 0.11), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.89, 0.13), True),
                                                            tobii.CalibrationEyeData((0.98, 0.09), True))))
        calibration_point3 = tobii.CalibrationPoint((0.5, 0.5),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.51, 0.51), True),
                                                            tobii.CalibrationEyeData((0.53, 0.45), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.43, 0.48), True),
                                                            tobii.CalibrationEyeData((0.49, 0.49), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.50, 0.53), True),
                                                            tobii.CalibrationEyeData((0.49, 0.54), True))))
        calibration_point4 = tobii.CalibrationPoint((0.1, 0.9),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.08, 0.98), True),
                                                            tobii.CalibrationEyeData((0.09, 0.8), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.12, 0.91), True),
                                                            tobii.CalibrationEyeData((0.18, 0.92), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.11, 0.92), True),
                                                            tobii.CalibrationEyeData((0.10, 0.90), True))))
        calibration_point5 = tobii.CalibrationPoint((0.9, 0.9),(
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.98, 0.98), True),
                                                            tobii.CalibrationEyeData((0.99, 0.98), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.92, 0.91), True),
                                                            tobii.CalibrationEyeData((0.98, 0.92), True)),
                                    tobii.CalibrationSample(tobii.CalibrationEyeData((0.91, 0.92), True),
                                                            tobii.CalibrationEyeData((0.90, 0.90), True))))
        calibration_points = (calibration_point0, calibration_point, calibration_point2,
                              calibration_point3, calibration_point4, calibration_point5)
        calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)                                                               
        calibData = tobii_helper._TobiiHelper__calculateCalibration(calibResult)
        self.assertEqual(5, len(calibData))
        self.assertEqual(4, len(calibData[0]))
        self.assertEqual(4, len(calibData[1]))
        self.assertEqual(4, len(calibData[2]))
        self.assertEqual(4, len(calibData[3]))
        self.assertEqual(4, len(calibData[4]))

        # (0.1,0.1)
        # average sample point
        self.assertEqual(-546, calibData[0][0][0])
        self.assertEqual(307, calibData[0][0][1])
        # average left eye sample point
        self.assertEqual(-541, calibData[0][1][0])
        self.assertEqual(304, calibData[0][1][1])
        # average right eye sample point
        self.assertEqual(-514, calibData[0][2][0])
        self.assertEqual(307, calibData[0][2][1])

        # (0.9,0.1)
        # average sample point
        self.assertEqual(546, calibData[1][0][0])
        self.assertEqual(307, calibData[1][0][1])
        # average left eye sample point
        self.assertEqual(582, calibData[1][1][0])
        self.assertEqual(299, calibData[1][1][1])
        # average right eye sample point
        self.assertEqual(623, calibData[1][2][0])
        self.assertEqual(309, calibData[1][2][1])

        # (0.5,0.5)
        # average sample point
        self.assertEqual(0, calibData[2][0][0])
        self.assertEqual(0, calibData[2][0][1])
        # average left eye sample point
        self.assertEqual(-27, calibData[2][1][0])
        self.assertEqual(-5, calibData[2][1][1])
        # average right eye sample point
        self.assertEqual(4, calibData[2][2][0])
        self.assertEqual(5, calibData[2][2][1])

        # (0.1,0.9)
        # average sample point
        self.assertEqual(-546, calibData[3][0][0])
        self.assertEqual(-307, calibData[3][0][1])
        # average left eye sample point
        self.assertEqual(-541, calibData[3][1][0])
        self.assertEqual(-335, calibData[3][1][1])
        # average right eye sample point
        self.assertEqual(-514, calibData[3][2][0])
        self.assertEqual(-286, calibData[3][2][1])

        # (0.9,0.9)
        # average sample point
        self.assertEqual(546, calibData[4][0][0])
        self.assertEqual(-307, calibData[4][0][1])
        # average left eye sample point
        self.assertEqual(596, calibData[4][1][0])
        self.assertEqual(-335, calibData[4][1][1])
        # average right eye sample point
        self.assertEqual(623, calibData[4][2][0])
        self.assertEqual(-332, calibData[4][2][1])        

if __name__ == "__main__":
    unittest.main() # run all tests