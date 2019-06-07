# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the calibrator module,
# test that instead of the system installed one.
sys.path = ["../tobii_calibration"] + ["../externals/psychopy_mock"] + sys.path

import tobii_calibration as calibrator

import psychopy_visual_mock as pvm
from psychopy import visual, logging

# ignore warnings comming from psychopy
logging.console.setLevel(logging.ERROR)

green_color = [-1.0, 1.0, -1.0]
red_color = [1.0, -1.0, -1.0]
yellow_color = [1.0, 1.0, 0.0]

def DummyFunction(*args):
    pass


class drawDistanceSliderTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())
        self.drawingWin = None

    def tearDown(self):
        if self.drawingWin is not None:
            self.drawingWin.close()

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
        self.initTrackBox(tobii_helper)
        tobii_helper.virtual_trackbox_width = 512.25
        tobii_helper.virtual_trackbox_height = 413.214

        self.drawingWin = visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])

    def testNotInitedThings(self):
        tobii_helper = calibrator.TobiiHelper()
        tobii_helper.disableLogging()

        tobii_helper._TobiiHelper__startGazeData = DummyFunction
        tobii_helper._TobiiHelper__stopGazeData = DummyFunction

        # no window
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__drawDistanceSlider([], [])

        # ok init the window
        with visual.Window(size = [1366, 768],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = tobii_helper.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4]) as drawingWin:

            # now we don't have a valid eye dist
            with self.assertRaises(TypeError):
                tobii_helper._TobiiHelper__drawDistanceSlider(drawingWin, [])

            # trackbox coordinates is not inited
            with self.assertRaises(RuntimeError):
                tobii_helper._TobiiHelper__drawDistanceSlider(drawingWin, 650)

            self.initTrackBox(tobii_helper)

            # no virtual trackbox sizes
            with self.assertRaises(RuntimeError):
                tobii_helper._TobiiHelper__drawDistanceSlider(drawingWin, 650)

            tobii_helper.virtual_trackbox_width = 512.25
            tobii_helper.virtual_trackbox_height = 413.214

            tobii_helper._TobiiHelper__drawDistanceSlider(drawingWin, 650)

    def testEyeInTrackbox(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 650)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # first object is the red rectangle on the top of the slider
        invalid_top = drawing_list[0]
        self.assertTrue(isinstance(invalid_top, pvm.Rect))
        # size
        self.assertAlmostEqual(10, invalid_top.width, delta = 0.001)
        self.assertAlmostEqual(51.651, invalid_top.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(306.125, invalid_top.pos[0], delta = 0.001)
        self.assertAlmostEqual(180.781, invalid_top.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, invalid_top.fillColor.tolist())

        # second object is the yellow rectangle on the top of the slider
        medium_top = drawing_list[1]
        self.assertTrue(isinstance(medium_top, pvm.Rect))
        # size
        self.assertAlmostEqual(10, medium_top.width, delta = 0.001)
        self.assertAlmostEqual(51.651, medium_top.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(306.125, medium_top.pos[0], delta = 0.001)
        self.assertAlmostEqual(129.129, medium_top.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, medium_top.fillColor.tolist())

        # third object is the green rectangle on the middle
        valid_region = drawing_list[2]
        self.assertTrue(isinstance(valid_region, pvm.Rect))
        # size
        self.assertAlmostEqual(10, valid_region.width, delta = 0.001)
        self.assertAlmostEqual(206.607, valid_region.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(306.125, valid_region.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.0, valid_region.pos[1], delta = 0.001)
        # color
        self.assertEqual(green_color, valid_region.fillColor.tolist())

        # forth object is the yellow rectangle on the bottom
        valid_region = drawing_list[3]
        self.assertTrue(isinstance(valid_region, pvm.Rect))
        # size
        self.assertAlmostEqual(10, valid_region.width, delta = 0.001)
        self.assertAlmostEqual(51.651, valid_region.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(306.125, valid_region.pos[0], delta = 0.001)
        self.assertAlmostEqual(-129.129, valid_region.pos[1], delta = 0.001)
        # color
        self.assertEqual(yellow_color, valid_region.fillColor.tolist())

        # fifth object is the red rectangle on the bottom
        valid_region = drawing_list[4]
        self.assertTrue(isinstance(valid_region, pvm.Rect))
        # size
        self.assertAlmostEqual(10, valid_region.width, delta = 0.001)
        self.assertAlmostEqual(51.651, valid_region.height, delta = 0.001)
        # pos
        self.assertAlmostEqual(306.125, valid_region.pos[0], delta = 0.001)
        self.assertAlmostEqual(-180.781, valid_region.pos[1], delta = 0.001)
        # color
        self.assertEqual(red_color, valid_region.fillColor.tolist())

        # sixth object is the marker in the slider on the bottom
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        # size
        self.assertAlmostEqual(10, marker.radius, delta = 0.001)
        # pos
        self.assertAlmostEqual(316.125, marker.pos[0], delta = 0.001)
        self.assertAlmostEqual(0.0, marker.pos[1], delta = 0.001)
        # orientation
        self.assertAlmostEqual(270.00, marker.ori, delta = 0.001)
        # color
        self.assertEqual([-0.8, -0.8, -0.8], marker.fillColor.tolist())

    def testEyeIsTooFar(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 830)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(-185.946, marker.pos[1], delta = 0.001)

    def testEyeIsEvenMoreFar(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 900)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(-206.607, marker.pos[1], delta = 0.001)

    def testEyeIsAlmostTooFar(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 795)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(-149.790, marker.pos[1], delta = 0.001)

    def testEyeIsTooNear(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 481)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(174.582, marker.pos[1], delta = 0.001)

    def testEyeIsEvenMoreNear(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 430)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(206.607, marker.pos[1], delta = 0.001)

    def testEyeIsAlmostNear(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 510)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(144.624, marker.pos[1], delta = 0.001)

    def testNoValidEyeData(self):
        tobii_helper = calibrator.TobiiHelper()
        self.initAll(tobii_helper)
        visual_mock = pvm.PsychoPyVisualMock()
        tobii_helper._TobiiHelper__drawDistanceSlider(self.drawingWin, 0)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(6, len(drawing_list))

        # checking marker pos
        marker = drawing_list[5]
        self.assertTrue(isinstance(marker, pvm.Polygon))
        self.assertAlmostEqual(206.607, marker.pos[1], delta = 0.001)



if __name__ == "__main__":
    unittest.main() # run all tests