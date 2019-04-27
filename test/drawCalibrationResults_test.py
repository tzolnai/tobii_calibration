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
import collections

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

class DummyClass:
    def leave_calibration_mode():
        pass

class drawCalibrationResultTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())
        self.calibWin = None

    def tearDown(self):
        if self.calibWin is not None:
            self.calibWin.close()

    def initAll(self, tobii_helper):
        tobii_helper.calibration = DummyClass
        tobii_helper.disableLogging()
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
        self.calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)
        self.calibWin = visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)), ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
        self.calibDict = collections.OrderedDict(pointList)

    def testNotInitedThingOrWrongParam(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        # no calibration
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__drawCalibrationResults(None, None, None)

        tobii_helper.calibration = "dummy"

        # no calibration results
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawCalibrationResults(None, None, None)

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
        calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)

        # no window
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawCalibrationResults(calibResult, None, None)

        calibWin = visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])

        # no calib points
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawCalibrationResults(calibResult, calibWin, None)

        pointList = [('1',(0.1, 0.1))]
        calibDict = collections.OrderedDict(pointList)

        # inconsitent data: calibDict has less items as calibResult
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawCalibrationResults(calibResult, calibWin, calibDict)

        pointList = [('1',(0.1, 0.1)), ('2',(0.5, 0.5))]
        calibDict = collections.OrderedDict(pointList)

        # inconsitent data: calibDict has different items as calibResult
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawCalibrationResults(calibResult, calibWin, calibDict)

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.9))]
        calibDict = collections.OrderedDict(pointList)

        # we are good now
        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper._TobiiHelper__drawCalibrationResults(calibResult, calibWin, calibDict)

        calibWin.close()

    def testTwoCalibPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

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
        self.calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.9))]
        self.calibDict = collections.OrderedDict(pointList)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(10, len(drawing_list))

        # first calib point's circle
        calibPoint1_circle = drawing_list[0]
        self.assertTrue(isinstance(calibPoint1_circle, pvm.Circle))
        # size
        self.assertEqual(50, calibPoint1_circle.radius)
        # pos
        self.assertEqual(-546, calibPoint1_circle.pos[0])
        self.assertEqual(307, calibPoint1_circle.pos[1])
        # color
        self.assertEqual([0.4, 0.4, 0.4], calibPoint1_circle.fillColor.tolist())
        self.assertEqual([1.0, 1.0, 1.0], calibPoint1_circle.lineColor.tolist())

        # first calib point's text
        calibPoint1_text = drawing_list[1]
        self.assertTrue(isinstance(calibPoint1_text, pvm.TextStim))
        # size
        self.assertEqual(60, calibPoint1_text.height)
        # pos
        self.assertEqual(-546, calibPoint1_text.pos[0])
        self.assertEqual(307, calibPoint1_text.pos[1])
        # color
        self.assertEqual([0.8, 0.8, 0.8], calibPoint1_text.color.tolist())
        # text
        self.assertEqual(str("1") , calibPoint1_text.text)

        # first calib point's left eye line
        calibPoint1_left_eye = drawing_list[2]
        self.assertTrue(isinstance(calibPoint1_left_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint1_left_eye.lineWidth)
        # pos
        self.assertEqual(-546, calibPoint1_left_eye.start[0])
        self.assertEqual(307, calibPoint1_left_eye.start[1])
        self.assertEqual(-541, calibPoint1_left_eye.end[0])
        self.assertEqual(304, calibPoint1_left_eye.end[1])
        # color
        self.assertEqual("yellow", calibPoint1_left_eye.lineColor)

        # first calib point's right eye line
        calibPoint1_right_eye = drawing_list[3]
        self.assertTrue(isinstance(calibPoint1_right_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint1_right_eye.lineWidth)
        # pos
        self.assertEqual(-546, calibPoint1_right_eye.start[0])
        self.assertEqual(307, calibPoint1_right_eye.start[1])
        self.assertEqual(-514, calibPoint1_right_eye.end[0])
        self.assertEqual(307, calibPoint1_right_eye.end[1])
        # color
        self.assertEqual("red", calibPoint1_right_eye.lineColor)

        # second calib point's circle
        calibPoint2_circle = drawing_list[4]
        self.assertTrue(isinstance(calibPoint2_circle, pvm.Circle))
        # size
        self.assertEqual(50, calibPoint2_circle.radius)
        # pos
        self.assertEqual(546, calibPoint2_circle.pos[0])
        self.assertEqual(-307, calibPoint2_circle.pos[1])
        # color
        self.assertEqual([0.4, 0.4, 0.4], calibPoint2_circle.fillColor.tolist())
        self.assertEqual([1.0, 1.0, 1.0], calibPoint2_circle.lineColor.tolist())

        # second calib point's text
        calibPoint2_text = drawing_list[5]
        self.assertTrue(isinstance(calibPoint2_text, pvm.TextStim))
        # size
        self.assertEqual(60, calibPoint2_text.height)
        # pos
        self.assertEqual(546, calibPoint2_text.pos[0])
        self.assertEqual(-307, calibPoint2_text.pos[1])
        # color
        self.assertEqual([0.8, 0.8, 0.8], calibPoint2_text.color.tolist())
        # text
        self.assertEqual(str("2") , calibPoint2_text.text)

        # second calib point's left eye line
        calibPoint2_left_eye = drawing_list[6]
        self.assertTrue(isinstance(calibPoint2_left_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint2_left_eye.lineWidth)
        # pos
        self.assertEqual(546, calibPoint2_left_eye.start[0])
        self.assertEqual(-307, calibPoint2_left_eye.start[1])
        self.assertEqual(582, calibPoint2_left_eye.end[0])
        self.assertEqual(-320, calibPoint2_left_eye.end[1])
        # color
        self.assertEqual("yellow", calibPoint2_left_eye.lineColor)

        # second calib point's right eye line
        calibPoint2_right_eye = drawing_list[7]
        self.assertTrue(isinstance(calibPoint2_right_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint2_right_eye.lineWidth)
        # pos
        self.assertEqual(546, calibPoint2_right_eye.start[0])
        self.assertEqual(-307, calibPoint2_right_eye.start[1])
        self.assertEqual(623, calibPoint2_right_eye.end[0])
        self.assertEqual(-368, calibPoint2_right_eye.end[1])
        # color
        self.assertEqual("red", calibPoint2_right_eye.lineColor)

        # text
        feedback_text = drawing_list[8]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Wait for the experimenter. \nUse number keys to select points for recalibration."), feedback_text.text)

        # text
        feedback_text = drawing_list[9]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Finished checking. Resuming calibration."), feedback_text.text)

    def testFiveCalibPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(22, len(drawing_list))

        for i in range(0,5):
            index = i * 4

            # calib point's circle
            calibPoint_circle = drawing_list[index]
            self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
            if i is 0:
                self.assertEqual(-546, calibPoint_circle.pos[0])
                self.assertEqual(307, calibPoint_circle.pos[1])
            elif i is 1:
                self.assertEqual(546, calibPoint_circle.pos[0])
                self.assertEqual(307, calibPoint_circle.pos[1])
            elif i is 2:
                self.assertEqual(0, calibPoint_circle.pos[0])
                self.assertEqual(0, calibPoint_circle.pos[1])
            elif i is 3:
                self.assertEqual(-546, calibPoint_circle.pos[0])
                self.assertEqual(-307, calibPoint_circle.pos[1])
            elif i is 4:
                self.assertEqual(546, calibPoint_circle.pos[0])
                self.assertEqual(-307, calibPoint_circle.pos[1])
            # color
            self.assertEqual([1.0, 1.0, 1.0], calibPoint_circle.lineColor.tolist())

            # calib point's text
            calibPoint_text = drawing_list[index + 1]
            self.assertTrue(isinstance(calibPoint_text, pvm.TextStim))
            if i is 0:
                self.assertEqual(-546, calibPoint_text.pos[0])
                self.assertEqual(307, calibPoint_text.pos[1])
                # text
                self.assertEqual(str("1") , calibPoint_text.text)
            elif i is 1:
                self.assertEqual(546, calibPoint_text.pos[0])
                self.assertEqual(307, calibPoint_text.pos[1])
                # text
                self.assertEqual(str("2") , calibPoint_text.text)
            elif i is 2:
                self.assertEqual(0, calibPoint_text.pos[0])
                self.assertEqual(0, calibPoint_text.pos[1])
                # text
                self.assertEqual(str("3") , calibPoint_text.text)
            elif i is 3:
                self.assertEqual(-546, calibPoint_text.pos[0])
                self.assertEqual(-307, calibPoint_text.pos[1])
                # text
                self.assertEqual(str("4") , calibPoint_text.text)
            elif i is 5:
                self.assertEqual(546, calibPoint_text.pos[0])
                self.assertEqual(-307, calibPoint_text.pos[1])
                # text
                self.assertEqual(str("5") , calibPoint_text.text)

            # calib point's left eye line
            calibPoint_left_eye = drawing_list[index + 2]
            self.assertTrue(isinstance(calibPoint_left_eye, pvm.Line))
            # pos
            if i is 0:
                self.assertEqual(-546, calibPoint_left_eye.start[0])
                self.assertEqual(307, calibPoint_left_eye.start[1])
                self.assertEqual(-541, calibPoint_left_eye.end[0])
                self.assertEqual(304, calibPoint_left_eye.end[1])
            elif i is 1:
                self.assertEqual(546, calibPoint_left_eye.start[0])
                self.assertEqual(307, calibPoint_left_eye.start[1])
                self.assertEqual(582, calibPoint_left_eye.end[0])
                self.assertEqual(299, calibPoint_left_eye.end[1])
            elif i is 2:
                self.assertEqual(0, calibPoint_left_eye.start[0])
                self.assertEqual(0, calibPoint_left_eye.start[1])
                self.assertEqual(-27, calibPoint_left_eye.end[0])
                self.assertEqual(-5, calibPoint_left_eye.end[1])
            elif i is 3:
                self.assertEqual(-546, calibPoint_left_eye.start[0])
                self.assertEqual(-307, calibPoint_left_eye.start[1])
                self.assertEqual(-541, calibPoint_left_eye.end[0])
                self.assertEqual(-335, calibPoint_left_eye.end[1])
            elif i is 4:
                self.assertEqual(546, calibPoint_left_eye.start[0])
                self.assertEqual(-307, calibPoint_left_eye.start[1])
                self.assertEqual(596, calibPoint_left_eye.end[0])
                self.assertEqual(-335, calibPoint_left_eye.end[1])

            # first calib point's right eye line
            calibPoint_right_eye = drawing_list[index + 3]
            self.assertTrue(isinstance(calibPoint_right_eye, pvm.Line))
            if i is 0:
                self.assertEqual(-546, calibPoint_right_eye.start[0])
                self.assertEqual(307, calibPoint_right_eye.start[1])
                self.assertEqual(-514, calibPoint_right_eye.end[0])
                self.assertEqual(307, calibPoint_right_eye.end[1])
            elif i is 1:
                self.assertEqual(546, calibPoint_right_eye.start[0])
                self.assertEqual(307, calibPoint_right_eye.start[1])
                self.assertEqual(623, calibPoint_right_eye.end[0])
                self.assertEqual(309, calibPoint_right_eye.end[1])
            elif i is 2:
                self.assertEqual(0, calibPoint_right_eye.start[0])
                self.assertEqual(0, calibPoint_right_eye.start[1])
                self.assertEqual(4, calibPoint_right_eye.end[0])
                self.assertEqual(5, calibPoint_right_eye.end[1])
            elif i is 3:
                self.assertEqual(-546, calibPoint_right_eye.start[0])
                self.assertEqual(-307, calibPoint_right_eye.start[1])
                self.assertEqual(-514, calibPoint_right_eye.end[0])
                self.assertEqual(-286, calibPoint_right_eye.end[1])
            elif i is 4:
                self.assertEqual(546, calibPoint_right_eye.start[0])
                self.assertEqual(-307, calibPoint_right_eye.start[1])
                self.assertEqual(623, calibPoint_right_eye.end[0])
                self.assertEqual(-332, calibPoint_right_eye.end[1])

        # text
        feedback_text = drawing_list[index + 4]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Wait for the experimenter. \nUse number keys to select points for recalibration."), feedback_text.text)

    def testNoReturnedValues(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])

        result = tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        self.assertEqual(0, len(result))

    def testHasOneRedoPoint(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['3', 'c'])

        result = tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        self.assertEqual(1, len(result))
        self.assertEqual(collections.OrderedDict([('3',(0.5, 0.5))]), result)

    def testHasSomeRedoPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['5', '1', '2', 'c'])

        result = tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        self.assertEqual(3, len(result))
        self.assertEqual(collections.OrderedDict([('5',(0.9, 0.9)), ('1',(0.1, 0.1)), ('2',(0.9, 0.1))]), result)

    def testRedundantRedoPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['1', '2', '1', '3', '3', '1', 'c'])

        result = tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        self.assertEqual(2, len(result))
        self.assertEqual(collections.OrderedDict([('2',(0.9, 0.1)), ('1',(0.1, 0.1))]), result)


    def testRedoPointDrawing(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['1', '4', 'c'])

        tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(64, len(drawing_list))

        # first calib point's color before pushing any button
        calibPoint_circle = drawing_list[0]
        self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
        self.assertEqual([1.0, 1.0, 1.0], calibPoint_circle.lineColor.tolist())

        # first calib point's color after first keyboard input
        calibPoint_circle = drawing_list[21]
        self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
        self.assertEqual([-1.0, 1.0, -1.0], calibPoint_circle.lineColor.tolist())

        # first calib point's color after second keyboard input
        calibPoint_circle = drawing_list[42]
        self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
        self.assertEqual([-1.0, 1.0, -1.0], calibPoint_circle.lineColor.tolist())

        # fifth calib point's color before pushing any button
        calibPoint_circle = drawing_list[12]
        self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
        self.assertEqual([1.0, 1.0, 1.0], calibPoint_circle.lineColor.tolist())

        # fifth calib point's color after first keyboard input
        calibPoint_circle = drawing_list[33]
        self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
        self.assertEqual([1.0, 1.0, 1.0], calibPoint_circle.lineColor.tolist())

        # fifth calib point's color after second keyboard input
        calibPoint_circle = drawing_list[54]
        self.assertTrue(isinstance(calibPoint_circle, pvm.Circle))
        self.assertEqual([-1.0, 1.0, -1.0], calibPoint_circle.lineColor.tolist())

    def testTwoCalibPointsWithoutNullItem(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

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
        calibration_points = (calibration_point, calibration_point2)
        self.calibResult = tobii.CalibrationResult(tobii.CALIBRATION_STATUS_SUCCESS, calibration_points)

        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.9))]
        self.calibDict = collections.OrderedDict(pointList)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(10, len(drawing_list))

        # first calib point's circle
        calibPoint1_circle = drawing_list[0]
        self.assertTrue(isinstance(calibPoint1_circle, pvm.Circle))
        # size
        self.assertEqual(50, calibPoint1_circle.radius)
        # pos
        self.assertEqual(-546, calibPoint1_circle.pos[0])
        self.assertEqual(307, calibPoint1_circle.pos[1])
        # color
        self.assertEqual([0.4, 0.4, 0.4], calibPoint1_circle.fillColor.tolist())
        self.assertEqual([1.0, 1.0, 1.0], calibPoint1_circle.lineColor.tolist())

        # first calib point's text
        calibPoint1_text = drawing_list[1]
        self.assertTrue(isinstance(calibPoint1_text, pvm.TextStim))
        # size
        self.assertEqual(60, calibPoint1_text.height)
        # pos
        self.assertEqual(-546, calibPoint1_text.pos[0])
        self.assertEqual(307, calibPoint1_text.pos[1])
        # color
        self.assertEqual([0.8, 0.8, 0.8], calibPoint1_text.color.tolist())
        # text
        self.assertEqual(str("1") , calibPoint1_text.text)

        # first calib point's left eye line
        calibPoint1_left_eye = drawing_list[2]
        self.assertTrue(isinstance(calibPoint1_left_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint1_left_eye.lineWidth)
        # pos
        self.assertEqual(-546, calibPoint1_left_eye.start[0])
        self.assertEqual(307, calibPoint1_left_eye.start[1])
        self.assertEqual(-541, calibPoint1_left_eye.end[0])
        self.assertEqual(304, calibPoint1_left_eye.end[1])
        # color
        self.assertEqual("yellow", calibPoint1_left_eye.lineColor)

        # first calib point's right eye line
        calibPoint1_right_eye = drawing_list[3]
        self.assertTrue(isinstance(calibPoint1_right_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint1_right_eye.lineWidth)
        # pos
        self.assertEqual(-546, calibPoint1_right_eye.start[0])
        self.assertEqual(307, calibPoint1_right_eye.start[1])
        self.assertEqual(-514, calibPoint1_right_eye.end[0])
        self.assertEqual(307, calibPoint1_right_eye.end[1])
        # color
        self.assertEqual("red", calibPoint1_right_eye.lineColor)

        # second calib point's circle
        calibPoint2_circle = drawing_list[4]
        self.assertTrue(isinstance(calibPoint2_circle, pvm.Circle))
        # size
        self.assertEqual(50, calibPoint2_circle.radius)
        # pos
        self.assertEqual(546, calibPoint2_circle.pos[0])
        self.assertEqual(-307, calibPoint2_circle.pos[1])
        # color
        self.assertEqual([0.4, 0.4, 0.4], calibPoint2_circle.fillColor.tolist())
        self.assertEqual([1.0, 1.0, 1.0], calibPoint2_circle.lineColor.tolist())

        # second calib point's text
        calibPoint2_text = drawing_list[5]
        self.assertTrue(isinstance(calibPoint2_text, pvm.TextStim))
        # size
        self.assertEqual(60, calibPoint2_text.height)
        # pos
        self.assertEqual(546, calibPoint2_text.pos[0])
        self.assertEqual(-307, calibPoint2_text.pos[1])
        # color
        self.assertEqual([0.8, 0.8, 0.8], calibPoint2_text.color.tolist())
        # text
        self.assertEqual(str("2") , calibPoint2_text.text)

        # second calib point's left eye line
        calibPoint2_left_eye = drawing_list[6]
        self.assertTrue(isinstance(calibPoint2_left_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint2_left_eye.lineWidth)
        # pos
        self.assertEqual(546, calibPoint2_left_eye.start[0])
        self.assertEqual(-307, calibPoint2_left_eye.start[1])
        self.assertEqual(582, calibPoint2_left_eye.end[0])
        self.assertEqual(-320, calibPoint2_left_eye.end[1])
        # color
        self.assertEqual("yellow", calibPoint2_left_eye.lineColor)

        # second calib point's right eye line
        calibPoint2_right_eye = drawing_list[7]
        self.assertTrue(isinstance(calibPoint2_right_eye, pvm.Line))
        # size
        self.assertEqual(20, calibPoint2_right_eye.lineWidth)
        # pos
        self.assertEqual(546, calibPoint2_right_eye.start[0])
        self.assertEqual(-307, calibPoint2_right_eye.start[1])
        self.assertEqual(623, calibPoint2_right_eye.end[0])
        self.assertEqual(-368, calibPoint2_right_eye.end[1])
        # color
        self.assertEqual("red", calibPoint2_right_eye.lineColor)

        # text
        feedback_text = drawing_list[8]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Wait for the experimenter. \nUse number keys to select points for recalibration."), feedback_text.text)

        # text
        feedback_text = drawing_list[9]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Finished checking. Resuming calibration."), feedback_text.text)

    def testQuitByQ(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])

        with self.assertRaises(SystemExit):
            tobii_helper._TobiiHelper__drawCalibrationResults(self.calibResult, self.calibWin, self.calibDict)

if __name__ == "__main__":
    unittest.main() # run all tests