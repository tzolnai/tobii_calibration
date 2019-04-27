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

from psychopy import visual, event, logging
import psychopy_visual_mock as pvm
from psychopy import core as pcore
import math
import collections

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

def DummyFunction(*argv):
    pass

calibrator.TobiiHelper._TobiiHelper__startGazeData = DummyFunction
calibrator.TobiiHelper._TobiiHelper__stopGazeData = DummyFunction
pcore.wait = DummyFunction

class DummyCalibration:
    def collect_data(*args):
        return tobii.CALIBRATION_STATUS_SUCCESS

    def discard_data(*args):
        pass

    def enter_calibration_mode(*args):
        pass

    def leave_calibration_mode(*args):
        pass

    def compute_and_apply(*args):
        return tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, ())

def createDummyCalibration(eyetracker):
    return DummyCalibration()

tobii.ScreenBasedCalibration = createDummyCalibration

class drawCalibrationScreenTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())
        self.calibWin = None

    def tearDown(self):
        if self.calibWin is not None:
            self.calibWin.close()

    def initAll(self, tobii_helper):

        def returnSuccess(*args):
            return tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, ())
        DummyCalibration.compute_and_apply = returnSuccess

        tobii_helper.disableLogging()
        tobii_helper.setMonitor(dimensions = (1366, 768))
        tobii_helper.eyetracker = "dummy"

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)), ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
        self.calibDict = collections.OrderedDict(pointList)

        self.calibWin = visual.Window(size = [1366, 768],
                                     pos = [0, 0],
                                     units = 'pix',
                                     fullscr = True,
                                     allowGUI = True,
                                     monitor = tobii_helper.win,
                                     winType = 'pyglet',
                                     color = [0.4, 0.4, 0.4])

        calibrator.TobiiHelper._TobiiHelper__drawCalibrationResults = DummyFunction # we tested this somewhere else


    def testWrongParam(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawCalibrationScreen(None, None)

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)), ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
        calibDict = collections.OrderedDict(pointList)

        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawCalibrationScreen(calibDict, None)

    def testNotInitedThings(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)), ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
        calibDict = collections.OrderedDict(pointList)

        calibWin = visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])

        # no monitor
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawCalibrationScreen(calibDict, calibWin)

        tobii_helper.setMonitor()

        # no eyetracker
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawCalibrationScreen(calibDict, calibWin)

        tobii_helper.eyetracker = "dummy"

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c', 'c'])

        # now we are good
        tobii_helper._TobiiHelper__drawCalibrationScreen(calibDict, calibWin)

        calibWin.close()

    def testNormalExecution(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c', 'c'])
        tobii_helper._TobiiHelper__drawCalibrationScreen(self.calibDict, self.calibWin)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 150 + 6, len(drawing_list))
        # 5 * 150 is drawn by __getCalibrationData() (tested in another test)

        # calibration message
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please focus your eyes on the red dot " + \
                             "and follow it with your eyes as closely as " + \
                             "possible.\n\nPress 'c' to continue."), message.text)
        # fix cross
        fixCross = drawing_list[1]
        self.assertTrue(isinstance(fixCross, pvm.TextStim))
        self.assertEqual(str("+"), fixCross.text)

        # doing __getCalibrationData()

        # then more messages
        message = drawing_list[752]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Applying calibration..."), message.text)

        message = drawing_list[753]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calculating calibration accuracy..."), message.text)

        message = drawing_list[754]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calibration was successful.\n\n" + \
                             "Moving on to validation."), message.text)

        message = drawing_list[755]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("+"), message.text)

    def testWithRedoPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        redoList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1))]

        # doing redoing
        def drawCalibrationResultsRedo(*args):
            if len(redoList) > 0:
                result = collections.OrderedDict(redoList)
                redoList.clear()
                return result

        calibrator.TobiiHelper._TobiiHelper__drawCalibrationResults = drawCalibrationResultsRedo

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c', 'c'])
        tobii_helper._TobiiHelper__drawCalibrationScreen(self.calibDict, self.calibWin)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(7 * 150 + 10, len(drawing_list))
        # 7 * 150 is drawn by __getCalibrationData() (tested in another test)

        # calibration message
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please focus your eyes on the red dot " + \
                             "and follow it with your eyes as closely as " + \
                             "possible.\n\nPress 'c' to continue."), message.text)
        # fix cross
        fixCross = drawing_list[1]
        self.assertTrue(isinstance(fixCross, pvm.TextStim))
        self.assertEqual(str("+"), fixCross.text)

        # doing __getCalibrationData()

        # then more messages
        message = drawing_list[752]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Applying calibration..."), message.text)

        message = drawing_list[753]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calculating calibration accuracy..."), message.text)

        # need one more round of calibration
        message = drawing_list[754]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calibration is almost complete.\n\n" + \
                             "Prepare to recalibrate a few points."), message.text)

        message = drawing_list[755]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("+"), message.text)

        message = drawing_list[1058]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calibration was successful.\n\n" + \
                             "Moving on to validation."), message.text)

        message = drawing_list[1059]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("+"), message.text)

    def testFailedCalibration(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        redoList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1))]

        def returnFailure(*args):
            return tobii.CalibrationResult(tobii.CALIBRATION_STATUS_FAILURE, ())

        DummyCalibration.compute_and_apply = returnFailure

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c', 'c'])
        tobii_helper._TobiiHelper__drawCalibrationScreen(self.calibDict, self.calibWin)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 150 + 3, len(drawing_list))
        # 5 * 150 is drawn by __getCalibrationData() (tested in another test)

        # calibration message
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please focus your eyes on the red dot " + \
                             "and follow it with your eyes as closely as " + \
                             "possible.\n\nPress 'c' to continue."), message.text)
        # fix cross
        fixCross = drawing_list[1]
        self.assertTrue(isinstance(fixCross, pvm.TextStim))
        self.assertEqual(str("+"), fixCross.text)

        # doing __getCalibrationData()

        # then message about the failure
        message = drawing_list[752]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calibration was not successful.\n\n" + \
                             "Closing the calibration window."), message.text)

    def testLeftEyeFailure(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        def returnFailure(*args):
            return tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS_RIGHT_EYE, ())

        DummyCalibration.compute_and_apply = returnFailure

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c', 'c'])
        tobii_helper._TobiiHelper__drawCalibrationScreen(self.calibDict, self.calibWin)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 150 + 3, len(drawing_list))
        # 5 * 150 is drawn by __getCalibrationData() (tested in another test)

        # calibration message
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please focus your eyes on the red dot " + \
                             "and follow it with your eyes as closely as " + \
                             "possible.\n\nPress 'c' to continue."), message.text)
        # fix cross
        fixCross = drawing_list[1]
        self.assertTrue(isinstance(fixCross, pvm.TextStim))
        self.assertEqual(str("+"), fixCross.text)

        # doing __getCalibrationData()

        # then message about the failure
        message = drawing_list[752]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calibration was not successful.\n\n" + \
                             "Closing the calibration window."), message.text)

    def testRigthEyeFailure(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        def returnFailure(*args):
            return tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS_LEFT_EYE, ())

        DummyCalibration.compute_and_apply = returnFailure

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c', 'c'])
        tobii_helper._TobiiHelper__drawCalibrationScreen(self.calibDict, self.calibWin)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 150 + 3, len(drawing_list))
        # 5 * 150 is drawn by __getCalibrationData() (tested in another test)

        # calibration message
        message = drawing_list[0]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Please focus your eyes on the red dot " + \
                             "and follow it with your eyes as closely as " + \
                             "possible.\n\nPress 'c' to continue."), message.text)
        # fix cross
        fixCross = drawing_list[1]
        self.assertTrue(isinstance(fixCross, pvm.TextStim))
        self.assertEqual(str("+"), fixCross.text)

        # doing __getCalibrationData()

        # then message about the failure
        message = drawing_list[752]
        self.assertTrue(isinstance(message, pvm.TextStim))
        self.assertEqual(str("Calibration was not successful.\n\n" + \
                             "Closing the calibration window."), message.text)

if __name__ == "__main__":
    unittest.main() # run all tests