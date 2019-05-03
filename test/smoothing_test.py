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

class getAvgEyeDistTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def testInvalidAverageCall(self):
        tobii_helper = calibrator.TobiiHelper()
        # invalid type
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__calcMeanOfPointList(1.1)

        # empty list
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__calcMeanOfPointList([])

        # list of number
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__calcMeanOfPointList([1.2])

        # list of tupple with wrong len
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__calcMeanOfPointList([(1.1)])

        # list of tupple of str pairs
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__calcMeanOfPointList([("2", "1")])

    def testOneItemAverage(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = [(0.2, 0.4)]
        result = tobii_helper._TobiiHelper__calcMeanOfPointList(point_list)
        self.assertAlmostEqual(0.2, result[0], delta = 0.001)
        self.assertAlmostEqual(0.4, result[1], delta = 0.001)

    def testNegativeAverage(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = [(-0.22, -0.41), (-0.18, -0.5)]
        result = tobii_helper._TobiiHelper__calcMeanOfPointList(point_list)
        self.assertAlmostEqual(-0.2, result[0], delta = 0.001)
        self.assertAlmostEqual(-0.454, result[1], delta = 0.001)

    def testOddNumbersAverage(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = [(0.22, 0.41), (0.18, 0.5), (0.16, 0.45)]
        result = tobii_helper._TobiiHelper__calcMeanOfPointList(point_list)
        self.assertAlmostEqual(0.186, result[0], delta = 0.001)
        self.assertAlmostEqual(0.454, result[1], delta = 0.001)

    def testSmoothingOneItem(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0)], point_list)
        self.assertEqual((1.0, 1.0), result)

    def testSmoothingMoreItems(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0)], point_list)
        self.assertEqual((1.0, 1.0), result)
        result = tobii_helper._TobiiHelper__smoothing((1.2, 1.3), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0), (1.2, 1.3)], point_list)
        self.assertEqual((1.1, 1.15), result)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0), (1.2, 1.3), (0.8, 0.7)], point_list)
        self.assertEqual((1.0, 1.0), result)

    def testSmoothingInvalidItem(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.1, 1.3), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0), (1.1, 1.3), (0.8, 0.7)], point_list)
        self.assertAlmostEqual(0.966, result[0], delta = 0.001)
        self.assertAlmostEqual(1.0, result[1], delta = 0.001)

        result = tobii_helper._TobiiHelper__smoothing((0.99, 0.99), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.1, 1.3), (0.8, 0.7)], point_list) # one item is removed
        self.assertAlmostEqual(0.950, result[0], delta = 0.001)
        self.assertAlmostEqual(1.0, result[1], delta = 0.001)

    def testSmoothingLimitReached(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.1, 1.3), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.1, 1.3), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.1, 1.3), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)

        self.assertEqual([(1.1, 1.3), (0.8, 0.7), (1.0, 1.0), (1.1, 1.3), (0.8, 0.7)], point_list)
        self.assertAlmostEqual(0.966, result[0], delta = 0.001)
        self.assertAlmostEqual(1.0, result[1], delta = 0.001)

    def testSmoothingNumbers(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []
        # add some items
        result = tobii_helper._TobiiHelper__smoothing(1.0, point_list, 0.0, lambda list : sum(list) / len(list))
        result = tobii_helper._TobiiHelper__smoothing(1.3, point_list, 0.0, lambda list : sum(list) / len(list))
        result = tobii_helper._TobiiHelper__smoothing(0.8, point_list, 0.0, lambda list : sum(list) / len(list))
        self.assertEqual([1.0, 1.3, 0.8], point_list)
        self.assertAlmostEqual(1.033, result, delta = 0.001)

        # check invalid item
        result = tobii_helper._TobiiHelper__smoothing(0.0, point_list, 0.0, lambda list : sum(list) / len(list))
        self.assertEqual([1.3, 0.8], point_list)
        self.assertAlmostEqual(1.05, result, delta = 0.001)

    def testSmoothingNoValidData(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []

        result = tobii_helper._TobiiHelper__smoothing((0.99, 0.99), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([], point_list)
        self.assertAlmostEqual(0.99, result[0], delta = 0.001)
        self.assertAlmostEqual(0.99, result[1], delta = 0.001)

        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.1, 1.3), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0), (1.1, 1.3), (0.8, 0.7)], point_list)
        self.assertAlmostEqual(0.966, result[0], delta = 0.001)
        self.assertAlmostEqual(1.0, result[1], delta = 0.001)

        result = tobii_helper._TobiiHelper__smoothing((0.99, 0.99), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.99, 0.99), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(0.8, 0.7)], point_list)
        self.assertAlmostEqual(0.8, result[0], delta = 0.001)
        self.assertAlmostEqual(0.7, result[1], delta = 0.001)
        result = tobii_helper._TobiiHelper__smoothing((0.99, 0.99), point_list, (0.99, 0.99), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([], point_list)
        self.assertAlmostEqual(0.99, result[0], delta = 0.001)
        self.assertAlmostEqual(0.99, result[1], delta = 0.001)

    def testSmoothingInvalidItemNan(self):
        tobii_helper = calibrator.TobiiHelper()
        point_list = []
        result = tobii_helper._TobiiHelper__smoothing((1.0, 1.0), point_list, (math.nan, math.nan), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((1.1, 1.3), point_list, (math.nan, math.nan), tobii_helper._TobiiHelper__calcMeanOfPointList)
        result = tobii_helper._TobiiHelper__smoothing((0.8, 0.7), point_list, (math.nan, math.nan), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.0, 1.0), (1.1, 1.3), (0.8, 0.7)], point_list)
        self.assertAlmostEqual(0.966, result[0], delta = 0.001)
        self.assertAlmostEqual(1.0, result[1], delta = 0.001)

        result = tobii_helper._TobiiHelper__smoothing((math.nan, math.nan), point_list, (math.nan, math.nan), tobii_helper._TobiiHelper__calcMeanOfPointList)
        self.assertEqual([(1.1, 1.3), (0.8, 0.7)], point_list) # one item is removed
        self.assertAlmostEqual(0.950, result[0], delta = 0.001)
        self.assertAlmostEqual(1.0, result[1], delta = 0.001)

if __name__ == "__main__":
    unittest.main() # run all tests