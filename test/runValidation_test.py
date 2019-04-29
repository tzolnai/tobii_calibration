# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the calibrator module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + sys.path

import tobii_calibration as calibrator

from psychopy import visual, event, logging
import psychopy_visual_mock as pvm
from psychopy import core as pcore
import math
import collections

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

def DummyFunction(tobiiHelper):
    pass

calibrator.TobiiHelper._TobiiHelper__startGazeData = DummyFunction
calibrator.TobiiHelper._TobiiHelper__stopGazeData = DummyFunction

pcore.wait = DummyFunction

class runValidationTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())

    def initAll(self, tobii_helper):
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True

        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (0.34, 0.56)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (0.32, 0.61)

    def testWrongParam(self):
        tobii_helper = calibrator.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.runValidation([])

    def testNotInitedThings(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()

        # no monitor
        with self.assertRaises(RuntimeError):
            tobii_helper.runValidation()

        tobii_helper.setMonitor()

        # no eye tracker
        with self.assertRaises(RuntimeError):
            tobii_helper.runValidation()
        
        tobii_helper.eyetracker = "dummy"

        # no tracking
        with self.assertRaises(RuntimeError):
            tobii_helper.runValidation()

        tobii_helper.tracking = True

        # no gaze data
        with self.assertRaises(RuntimeError):
            tobii_helper.runValidation()
            
        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (0.34, 0.56)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (0.32, 0.6)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runValidation()

    def testDefaultFiveCalibPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runValidation()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(7, len(drawing_list))

        # first object is the gaze point
        eye_circle = drawing_list[0]
        self.assertTrue(isinstance(eye_circle, pvm.Circle))
        # size
        self.assertAlmostEqual(50, eye_circle.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(-232.0, eye_circle.pos[0], delta = 0.001)
        self.assertAlmostEqual(-65.0, eye_circle.pos[1], delta = 0.001)
        # color
        self.assertEqual([1.0, 1.0, 0.55], eye_circle.fillColor.tolist())
        self.assertEqual([1.0, 0.95, 0.0], eye_circle.lineColor.tolist())

        # the next five objects are the calibration points
        for i in range(1,6):
            calib_point = drawing_list[i]
            self.assertTrue(isinstance(calib_point, pvm.Circle))
            # size
            self.assertAlmostEqual(20, calib_point.radius, delta = 0.001)
             # pos
            if i == 1:
                self.assertAlmostEqual(-546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(307.00, calib_point.pos[1], delta = 0.001)
            elif i == 2:
                self.assertAlmostEqual(546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(307.00, calib_point.pos[1], delta = 0.001)
            elif i == 3:
                self.assertAlmostEqual(0.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(0.00, calib_point.pos[1], delta = 0.001)
            elif i == 4:
                self.assertAlmostEqual(-546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(-307.00, calib_point.pos[1], delta = 0.001)
            elif i == 5:
                self.assertAlmostEqual(546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(-307.00, calib_point.pos[1], delta = 0.001)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calib_point.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calib_point.lineColor.tolist())

        # last object is the text
        feedback_text = drawing_list[6]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(0.07, feedback_text.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, feedback_text.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.5, feedback_text.pos[1], delta = 0.001)
        # color
        self.assertEqual([0.4, 0.4, 0.4], feedback_text.color.tolist())
        # text
        self.assertEqual(str("Wait for the experimenter.") , feedback_text.text)

    def testNineCalibPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        pointList = [('1',(0.1, 0.1)), ('2',(0.5, 0.1)), ('3',(0.9, 0.1)),
                     ('4',(0.1, 0.5)), ('5',(0.5, 0.5)), ('6',(0.9, 0.5)),
                     ('7',(0.1, 0.9)), ('8',(0.5, 0.9)), ('9',(0.9, 0.9))]
        tobii_helper.runValidation(collections.OrderedDict(pointList))
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(11, len(drawing_list))

        # first object is the gaze point
        eye_circle = drawing_list[0]
        self.assertTrue(isinstance(eye_circle, pvm.Circle))
        # size
        self.assertAlmostEqual(50, eye_circle.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(-232.0, eye_circle.pos[0], delta = 0.001)
        self.assertAlmostEqual(-65.0, eye_circle.pos[1], delta = 0.001)
        # color
        self.assertEqual([1.0, 1.0, 0.55], eye_circle.fillColor.tolist())
        self.assertEqual([1.0, 0.95, 0.0], eye_circle.lineColor.tolist())

        # the next five objects are the calibration points
        for i in range(1,10):
            calib_point = drawing_list[i]
            self.assertTrue(isinstance(calib_point, pvm.Circle))
            # size
            self.assertAlmostEqual(20, calib_point.radius, delta = 0.001)
             # pos
            if i == 1:
                self.assertAlmostEqual(-546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(307.00, calib_point.pos[1], delta = 0.001)
            elif i == 2:
                self.assertAlmostEqual(0.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(307.00, calib_point.pos[1], delta = 0.001)
            elif i == 3:
                self.assertAlmostEqual(546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(307.00, calib_point.pos[1], delta = 0.001)
            elif i == 4:
                self.assertAlmostEqual(-546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(0.00, calib_point.pos[1], delta = 0.001)
            elif i == 5:
                self.assertAlmostEqual(0.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(0.00, calib_point.pos[1], delta = 0.001)
            elif i == 6:
                self.assertAlmostEqual(546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(0.00, calib_point.pos[1], delta = 0.001)
            elif i == 7:
                self.assertAlmostEqual(-546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(-307.00, calib_point.pos[1], delta = 0.001)
            elif i == 8:
                self.assertAlmostEqual(0.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(-307.00, calib_point.pos[1], delta = 0.001)
            elif i == 9:
                self.assertAlmostEqual(546.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(-307.00, calib_point.pos[1], delta = 0.001)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calib_point.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calib_point.lineColor.tolist())

        # last object is the text
        feedback_text = drawing_list[10]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(0.07, feedback_text.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, feedback_text.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.5, feedback_text.pos[1], delta = 0.001)
        # color
        self.assertEqual([0.4, 0.4, 0.4], feedback_text.color.tolist())
        # text
        self.assertEqual(str("Wait for the experimenter.") , feedback_text.text)

    def testTwoCalibPoints(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        pointList = [('1',(0.25, 0.5)), ('2',(0.75, 0.5))]
        tobii_helper.runValidation(collections.OrderedDict(pointList))
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # first object is the gaze point
        eye_circle = drawing_list[0]
        self.assertTrue(isinstance(eye_circle, pvm.Circle))
        # size
        self.assertAlmostEqual(50, eye_circle.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(-232.0, eye_circle.pos[0], delta = 0.001)
        self.assertAlmostEqual(-65.0, eye_circle.pos[1], delta = 0.001)
        # color
        self.assertEqual([1.0, 1.0, 0.55], eye_circle.fillColor.tolist())
        self.assertEqual([1.0, 0.95, 0.0], eye_circle.lineColor.tolist())

        # the next five objects are the calibration points
        for i in range(1,3):
            calib_point = drawing_list[i]
            self.assertTrue(isinstance(calib_point, pvm.Circle))
            # size
            self.assertAlmostEqual(20, calib_point.radius, delta = 0.001)
             # pos
            if i == 1:
                self.assertAlmostEqual(-341.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(0.00, calib_point.pos[1], delta = 0.001)
            elif i == 2:
                self.assertAlmostEqual(341.00, calib_point.pos[0], delta = 0.001)
                self.assertAlmostEqual(0.00, calib_point.pos[1], delta = 0.001)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calib_point.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calib_point.lineColor.tolist())

        # last object is the text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(0.07, feedback_text.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, feedback_text.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.5, feedback_text.pos[1], delta = 0.001)
        # color
        self.assertEqual([0.4, 0.4, 0.4], feedback_text.color.tolist())
        # text
        self.assertEqual(str("Wait for the experimenter.") , feedback_text.text)

    def testEyeOutOfScope(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (1.1, 0.56)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (1.04, 0.61)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runValidation()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # the next five objects are the calibration points
        for i in range(1,5):
            calib_point = drawing_list[i]
            self.assertTrue(isinstance(calib_point, pvm.Circle))

        # last object is the text
        feedback_text = drawing_list[5]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))

    def testInvalidEyePos(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_point_on_display_area'] = (math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_point_on_display_area'] = (math.nan, math.nan)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runValidation()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # the next five objects are the calibration points
        for i in range(1,5):
            calib_point = drawing_list[i]
            self.assertTrue(isinstance(calib_point, pvm.Circle))

        # last object is the text
        feedback_text = drawing_list[5]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))

    def testQuitByQ(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])
        with self.assertRaises(SystemExit):
            tobii_helper.runValidation()

    def testRunWithExistingWindow(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])

        with visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4]) as valWin:

            tobii_helper.runValidation(valWin = valWin)
            valWin.close()

    def testWrongWindowParam(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        with self.assertRaises(TypeError):
            tobii_helper.runValidation(valWin = [])


if __name__ == "__main__":
    unittest.main() # run all tests