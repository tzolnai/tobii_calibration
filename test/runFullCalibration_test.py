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

from psychopy import visual, event, logging
import psychopy_visual_mock as pvm
from psychopy import core as pcore
import math
import collections

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

def DummyFunction(*argv):
    pass

pcore.wait = DummyFunction

class runFullCalibrationTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def initAll(self, tobii_helper):
        tobii_helper.eyetracker = "dummy"
        tobii_helper.setMonitor()

        def runValidationDummy(calibDict, calibWin):
            self.calibDict = calibDict

        tobii_helper._TobiiHelper__drawCalibrationScreen = DummyFunction # we test this somewhere else
        tobii_helper.runTrackBox = DummyFunction # we test this somewhere else
        tobii_helper.runValidation = runValidationDummy # we test this somewhere else


    def testNotInitedThings(self):
        tobii_helper = wrapper.TobiiHelper()

        # wrong param
        with self.assertRaises(TypeError):
            tobii_helper.runFullCalibration([])

        # wrong param
        with self.assertRaises(ValueError):
            tobii_helper.runFullCalibration(13)

        # missing eye tracker
        with self.assertRaises(ValueError):
            tobii_helper.runFullCalibration()

        tobii_helper.eyetracker = "dummy"

        # no monitor
        with self.assertRaises(ValueError):
            tobii_helper.runFullCalibration()

        tobii_helper.setMonitor()

    def testDefaultCalibPoints(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runFullCalibration()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(2, len(drawing_list))
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please position yourself so that the\n" + \
                             "eye-tracker can locate your eyes." + \
                             "\n\nPress 'c' to continue."), message.text)

        message = drawing_list[1]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Finished validating the calibration.\n\n" +\
                             "Calibration is complete. Closing window."), message.text)

        # default is five calib points
        self.assertEqual(5, len(self.calibDict))
        self.assertTrue('1' in self.calibDict)
        self.assertTrue('2' in self.calibDict)
        self.assertTrue('3' in self.calibDict)
        self.assertTrue('4' in self.calibDict)
        self.assertTrue('5' in self.calibDict)
        self.assertEqual((0.1, 0.1), self.calibDict['1'])
        self.assertEqual((0.9, 0.1), self.calibDict['2'])
        self.assertEqual((0.5, 0.5), self.calibDict['3'])
        self.assertEqual((0.1, 0.9), self.calibDict['4'])
        self.assertEqual((0.9, 0.9), self.calibDict['5'])

    def testNineCalibPoints(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runFullCalibration(9)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(2, len(drawing_list))
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please position yourself so that the\n" + \
                             "eye-tracker can locate your eyes." + \
                             "\n\nPress 'c' to continue."), message.text)

        message = drawing_list[1]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Finished validating the calibration.\n\n" +\
                             "Calibration is complete. Closing window."), message.text)

        self.assertEqual(9, len(self.calibDict))
        self.assertTrue('1' in self.calibDict)
        self.assertTrue('2' in self.calibDict)
        self.assertTrue('3' in self.calibDict)
        self.assertTrue('4' in self.calibDict)
        self.assertTrue('5' in self.calibDict)
        self.assertTrue('6' in self.calibDict)
        self.assertTrue('7' in self.calibDict)
        self.assertTrue('8' in self.calibDict)
        self.assertTrue('9' in self.calibDict)
        self.assertEqual((0.1, 0.1), self.calibDict['1'])
        self.assertEqual((0.5, 0.1), self.calibDict['2'])
        self.assertEqual((0.9, 0.1), self.calibDict['3'])
        self.assertEqual((0.1, 0.5), self.calibDict['4'])
        self.assertEqual((0.5, 0.5), self.calibDict['5'])
        self.assertEqual((0.9, 0.5), self.calibDict['6'])
        self.assertEqual((0.1, 0.9), self.calibDict['7'])
        self.assertEqual((0.5, 0.9), self.calibDict['8'])
        self.assertEqual((0.9, 0.9), self.calibDict['9'])

if __name__ == "__main__":
    unittest.main() # run all tests