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

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

green_color = [-1.0, 1.0, -1.0]
red_color = [1.0, -1.0, -1.0]
yellow_color = [1.0, 1.0, 0.0]

def DummyFunction(*args):
    pass

pcore.wait = DummyFunction

class runTrackBoxTest(unittest.TestCase):

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
        tobii_helper.tbCoordinates['frontDistance'] = 500.0
        tobii_helper.tbCoordinates['backDistance'] = 800.0

    def initAll(self, tobii_helper):
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        self.initTrackBox(tobii_helper)
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True

        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.0)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = True

        tobii_helper._TobiiHelper__drawDistanceSlider = DummyFunction
        tobii_helper._TobiiHelper__startGazeData = DummyFunction
        tobii_helper._TobiiHelper__stopGazeData = DummyFunction

    def testNotInitedThings(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()

        tobii_helper._TobiiHelper__startGazeData = DummyFunction
        tobii_helper._TobiiHelper__stopGazeData = DummyFunction

        # no window
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawEyePositions([])

        # ok init the window
        trackWin = visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])

        # now we don't have tracker box coordinates
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        self.initTrackBox(tobii_helper)

        # no eyetracker
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        tobii_helper.eyetracker = "dummy"

        # no tracking
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        tobii_helper.tracking = True

        # no gaze data
        with self.assertRaises(RuntimeError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.0)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = True

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper._TobiiHelper__drawEyePositions(trackWin)
        trackWin.close()

    def testNegativEyeData(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (-0.34, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        #first object is the background of the virtual trackbox
        background_rect = drawing_list[0]
        self.assertTrue(isinstance(background_rect, pvm.Rect))
        # size
        self.assertAlmostEqual(512.25, background_rect.width, delta = 0.001)
        self.assertAlmostEqual(413.215, background_rect.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, background_rect.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.0, background_rect.pos[1], delta = 0.001)

        #second object is the left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # size
        self.assertAlmostEqual(30, left_eye.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(430.29, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # size
        self.assertAlmostEqual(30, right_eye.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, right_eye.fillColor.tolist())
        self.assertEqual(green_color, right_eye.lineColor.tolist())

        #fourth object is the text about the distance
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(0.07, feedback_text.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, feedback_text.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.638, feedback_text.pos[1], delta = 0.001)
        # color
        self.assertEqual([1.0, 1.0, 1.0], feedback_text.color.tolist())
        # text
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testEyePosInTrackbox(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        #first object is the background of the virtual trackbox
        background_rect = drawing_list[0]
        self.assertTrue(isinstance(background_rect, pvm.Rect))
        # size
        self.assertAlmostEqual(512.25, background_rect.width, delta = 0.001)
        self.assertAlmostEqual(413.215, background_rect.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, background_rect.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.0, background_rect.pos[1], delta = 0.001)

        #second object is the left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # size
        self.assertAlmostEqual(30, left_eye.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, left_eye.fillColor.tolist())
        self.assertEqual(green_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # size
        self.assertAlmostEqual(30, right_eye.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, right_eye.fillColor.tolist())
        self.assertEqual(green_color, right_eye.lineColor.tolist())

        #fourth object is the text about the distance
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        # size
        self.assertAlmostEqual(0.07, feedback_text.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, feedback_text.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.638, feedback_text.pos[1], delta = 0.001)
        # color
        self.assertEqual([1.0, 1.0, 1.0], feedback_text.color.tolist())
        # text
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testEyeIsTooFar(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 1.0)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 1.0)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 820.9)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 820.7)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort."), feedback_text.text)

    def testEyeIsAlmostTooFar(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.97)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.97)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 780.8)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 780.5)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testEyeIsTooNear(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.5)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.5)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 440.9)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 440.7)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort."), feedback_text.text)

    def testEyeIsAlmostTooNear(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.97)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.97)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 505.8)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 515.5)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testNoValidEyeData(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (math.nan, math.nan, math.nan)
        tobii_helper.gazeData['left_gaze_origin_validity'] = False
        tobii_helper.gazeData['right_gaze_origin_validity'] = False

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(2, len(drawing_list)) # eye are not drawn

        # text
        feedback_text = drawing_list[1]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testDifferentFrontDistance(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.5)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.5)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 440.9)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 440.7)

        tobii_helper.tbCoordinates['frontDistance'] = 300.0
        tobii_helper.tbCoordinates['backDistance'] = 800.0

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, left_eye.fillColor.tolist())
        self.assertEqual(green_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, right_eye.fillColor.tolist())
        self.assertEqual(green_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort."), feedback_text.text)

    def testDifferentBackDistance(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        tobii_helper.tbCoordinates['frontDistance'] = 300.0
        tobii_helper.tbCoordinates['backDistance'] = 500.0

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testOneEyeIsFar(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.97)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 1.00)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 798.8)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 812.5)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(81.959, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-24.792, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(92.204, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-45.453, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("Press 'c' to calibrate or 'q' to abort.") , feedback_text.text)

    def testLeftEyeAlmosOutOnLeft(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.1, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # color
        self.assertEqual(green_color, right_eye.fillColor.tolist())
        self.assertEqual(green_color, right_eye.lineColor.tolist())

    def testLeftEyeOutOnLeft(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (-0.01, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.10, 0.61, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

    def testRightEyeAlmosOutOnRight(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.90, 0.43, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # color
        self.assertEqual(green_color, left_eye.fillColor.tolist())
        self.assertEqual(green_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

    def testRightEyeOutOnRight(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.98, 0.43, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (1.0001, 0.45, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

    def testRightEyeOutOnTop(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.93, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 1.001, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

    def testLeftEyeOutOnBottom(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, -1.001, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.11, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.2)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])
        tobii_helper.runTrackBox()
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(4, len(drawing_list))

        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

    def testQuitByQ(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])

        with self.assertRaises(SystemExit):
            tobii_helper.runTrackBox()

    def testRunWithExistingWindow(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])

        trackWin = visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])

        tobii_helper.runTrackBox(trackWin)
        trackWin.close()

    def testWrongWindowParam(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['c'])

        with self.assertRaises(TypeError):
            tobii_helper.runTrackBox(trackWin = [])

if __name__ == "__main__":
    unittest.main() # run all tests