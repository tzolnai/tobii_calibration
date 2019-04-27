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

def DummyFunction(tobiiHelper):
    pass

calibrator.TobiiHelper._TobiiHelper__startGazeData = DummyFunction
calibrator.TobiiHelper._TobiiHelper__stopGazeData = DummyFunction

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

    def initDisplayArea(self, tobii_helper):
        tobii_helper.adaCoordinates = {}
        tobii_helper.adaCoordinates['bottomLeft'] = (-237.45, 13.21, -10.88)
        tobii_helper.adaCoordinates['bottomRight'] = (239.19, 13.21, -10.88)
        tobii_helper.adaCoordinates['topLeft'] = (-237.45, 259.32, 93.58)
        tobii_helper.adaCoordinates['topRight'] = (239.19, 259.32, 93.58)
        tobii_helper.adaCoordinates['height'] = 267.36
        tobii_helper.adaCoordinates['width'] = 476.64

    def initAll(self, tobii_helper):
        tobii_helper.disableLogging()
        tobii_helper.setMonitor()
        self.initTrackBox(tobii_helper)
        self.initDisplayArea(tobii_helper)
        tobii_helper.eyetracker = "dummy"
        tobii_helper.tracking = True

        tobii_helper.gazeData = {}
        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (0.34, 0.56, 0.81)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.815)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 650.0)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 652.0)
        tobii_helper.gazeData['left_gaze_origin_validity'] = True
        tobii_helper.gazeData['right_gaze_origin_validity'] = True

    def testNotInitedThings(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()
        # no window
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        self.initTrackBox(tobii_helper)
        self.initDisplayArea(tobii_helper)

        # no eyetracker
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        tobii_helper.eyetracker = "dummy"

        # no tracking
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__drawEyePositions(trackWin)

        tobii_helper.tracking = True

        # no gaze data
        with self.assertRaises(ValueError):
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

        tobii_helper.gazeData['left_gaze_origin_in_trackbox_coordinate_system'] = (-0.34, 0.56, 0.5)
        tobii_helper.gazeData['right_gaze_origin_in_trackbox_coordinate_system'] = (0.32, 0.61, 0.5)
        tobii_helper.gazeData['left_gaze_origin_in_user_coordinate_system'] = (102.0, 135.52, 440.9)
        tobii_helper.gazeData['right_gaze_origin_in_user_coordinate_system'] = (96.0, 147.62, 440.7)

        with self.assertRaises(ValueError):
            tobii_helper.runTrackBox()

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
        self.assertAlmostEqual(0.629, background_rect.width, delta = 0.001)
        self.assertAlmostEqual(0.905, background_rect.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.0, background_rect.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.0, background_rect.pos[1], delta = 0.001)

        #second object is the left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # size
        self.assertAlmostEqual(0.07, left_eye.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, left_eye.fillColor.tolist())
        self.assertEqual(green_color, left_eye.lineColor.tolist())

        #third object is the right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # size
        self.assertAlmostEqual(0.07, right_eye.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
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
        self.assertAlmostEqual(-0.65, feedback_text.pos[1], delta = 0.001)
        # color
        self.assertEqual([1.0, 1.0, 1.0], feedback_text.color.tolist())
        # text
        self.assertEqual(str("You're currently 65 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort.") , feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 82 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort."), feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 78 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort.") , feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 44 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort."), feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, left_eye.fillColor.tolist())
        self.assertEqual(yellow_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, right_eye.fillColor.tolist())
        self.assertEqual(yellow_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 51 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort.") , feedback_text.text)

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

        self.assertEqual(4, len(drawing_list))

        # left eye
        left_eye = drawing_list[1]
        self.assertTrue(isinstance(left_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.99, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.99, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual([0.4, 0.4, 0.4], left_eye.fillColor.tolist())
        self.assertEqual([0.4, 0.4, 0.4], left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.99, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.99, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual([0.4, 0.4, 0.4], right_eye.fillColor.tolist())
        self.assertEqual([0.4, 0.4, 0.4], right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 0 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort.") , feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, left_eye.fillColor.tolist())
        self.assertEqual(green_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, right_eye.fillColor.tolist())
        self.assertEqual(green_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 44 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort."), feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 65 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort.") , feedback_text.text)

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
        self.assertAlmostEqual(0.171, left_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.054, left_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, left_eye.fillColor.tolist())
        self.assertEqual(red_color, left_eye.lineColor.tolist())

        # right eye
        right_eye = drawing_list[2]
        self.assertTrue(isinstance(right_eye, pvm.Circle))
        # pos
        self.assertAlmostEqual(0.192, right_eye.pos[0], delta = 0.001)
        self.assertAlmostEqual(-0.099, right_eye.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, right_eye.fillColor.tolist())
        self.assertEqual(red_color, right_eye.lineColor.tolist())

        # text
        feedback_text = drawing_list[3]
        self.assertTrue(isinstance(feedback_text, pvm.TextStim))
        self.assertEqual(str("You're currently 80 cm away from the screen. \nPress 'c' to calibrate or 'q' to abort.") , feedback_text.text)

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