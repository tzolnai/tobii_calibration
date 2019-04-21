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
from psychopy import visual, event
import psychopy_visual_mock as pvm
from psychopy import core as pcore
import collections

def DummyFunction(time):
    pass

pcore.wait = DummyFunction

class DummyCalibration:
    def collect_data(posx, posy):
        return tobii.CALIBRATION_STATUS_SUCCESS

    def leave_calibration_mode():
        pass

    def compute_and_apply():
        return []

class getCalibrationDataTest(unittest.TestCase):

    def setUp(self):
        print ("Current test: ", self.id())
        self.calibWin = None

    def tearDown(self):
        if self.calibWin is not None:
            self.calibWin.close()

    def initAll(self, tobii_helper):
        tobii_helper.calibration = DummyCalibration
        tobii_helper.setMonitor(dimensions = (1366, 768))

        self.calibWin = visual.Window(size = [1366, 768],
                         pos = [0, 0],
                         units = 'pix',
                         fullscr = True,
                         allowGUI = True,
                         monitor = tobii_helper.win,
                         winType = 'pyglet',
                         color = [0.4, 0.4, 0.4])

        self.pointList = [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.9, 0.9)]

    def testNotInitedThingOrWrongParam(self):
        tobii_helper = wrapper.TobiiHelper()

        # no calibration
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getCalibrationData(None, None)

        tobii_helper.calibration = DummyCalibration

        # no window
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__getCalibrationData(None, None)

        calibWin = visual.Window(size = [1366, 768],
                         pos = [0, 0],
                         units = 'pix',
                         fullscr = True,
                         allowGUI = True,
                         monitor = tobii_helper.win,
                         winType = 'pyglet',
                         color = [0.4, 0.4, 0.4])

        # no point list
        with self.assertRaises(TypeError):
            tobii_helper._TobiiHelper__getCalibrationData(calibWin, None)

        pointList = [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.9, 0.9)]

        # no monitor
        with self.assertRaises(ValueError):
            tobii_helper._TobiiHelper__getCalibrationData(calibWin, pointList)

        tobii_helper.setMonitor()

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])

        # now we are good
        tobii_helper._TobiiHelper__getCalibrationData(calibWin, pointList)

        calibWin.close()

    def testTwoCalibPoints(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)

        self.pointList = [(0.1, 0.1), (0.9, 0.9)]

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])
        tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(2 * 149, len(drawing_list))

        # first 49 frame is about moving the circle to the next calib point
        for i in range(0, 49):
            calibPoint = drawing_list[i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertEqual(50, calibPoint.radius)
            # pos
            self.assertAlmostEqual(524 - i * 22, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(-294 + i * 12, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

        # after the moving, circle is at the first calib point
        self.assertEqual(-524, drawing_list[48].pos[0])
        self.assertEqual(294, drawing_list[48].pos[1])

        # shrink the circle in 50 steps
        for i in range(0,50):
            calibPoint = drawing_list[49 + i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertAlmostEqual(50 - (i + 1) * 0.9, calibPoint.radius)
            # pos
            self.assertAlmostEqual(-524, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(294, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

        # return point to the original size in 50 steps
        for i in range(0,50):
            calibPoint = drawing_list[99 + i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertAlmostEqual(5 + (i + 1) * 0.9, calibPoint.radius)
            # pos
            self.assertAlmostEqual(-524, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(294, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

        # now do the same for the second calibration point

        # first 49 frame is about moving the circle to the next calib point
        for i in range(0,49):
            calibPoint = drawing_list[149 + i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertEqual(50, calibPoint.radius)
            # pos
            self.assertAlmostEqual(-524 + i * 22, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(294 - i * 12, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

        # after the moving, circle is at the first calib point
        self.assertEqual(524, drawing_list[197].pos[0])
        self.assertEqual(-294, drawing_list[197].pos[1])

        # shrink the circle in 50 steps
        for i in range(0,50):
            calibPoint = drawing_list[198 + i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertAlmostEqual(50 - (i + 1) * 0.9, calibPoint.radius)
            # pos
            self.assertAlmostEqual(524, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(-294, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

        # return point to the original size in 50 steps
        for i in range(0,50):
            calibPoint = drawing_list[248 + i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertAlmostEqual(5 + (i + 1) * 0.9, calibPoint.radius)
            # pos
            self.assertAlmostEqual(524, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(-294, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

    def testFiveCalibPoints(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])
        tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 149, len(drawing_list))

        for j in range(5):
            # first 49 frame is about moving the circle to the next calib point
            for i in range(0, 49):
                calibPoint = drawing_list[i + j * 149]
                self.assertTrue(isinstance(calibPoint, pvm.Circle))
                # size
                self.assertEqual(50, calibPoint.radius)
                if j is 0:
                    self.assertAlmostEqual(524 - i * 22, calibPoint.pos[0], delta = 10.0)
                    self.assertAlmostEqual(-294 + i * 12, calibPoint.pos[1], delta = 13.0)
                elif j is 1:
                    self.assertAlmostEqual(-524 + i * 22, calibPoint.pos[0], delta = 10.0)
                    self.assertEqual(307, calibPoint.pos[1]) # no vertical movement
                elif j is 2:
                    self.assertAlmostEqual(535 - i * 11, calibPoint.pos[0], delta = 10.0)
                    self.assertAlmostEqual(307 - i * 6, calibPoint.pos[1], delta = 13.0)
                elif j is 3:
                    self.assertAlmostEqual(0 - i * 11, calibPoint.pos[0], delta = 10.0)
                    self.assertAlmostEqual(0 - i * 6, calibPoint.pos[1], delta = 13.0)
                elif j is 4:
                    self.assertAlmostEqual(-524 + i * 22, calibPoint.pos[0], delta = 10.0)
                    self.assertEqual(-307, calibPoint.pos[1]) # no vertical movement
                # color
                self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
                self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

            # after the moving, circle is at the first calib point
            if j is 0:
                finalPos = (-524, 294) # bug: this should be 307
            elif j is 1:
                finalPos = (524, 307)
            elif j is 2:
                finalPos = (10, 6) # bug: this should be (0, 0)
            elif j is 3:
                finalPos = (-535, -301) # bug
            elif j is 4:
                finalPos = (524, -307) # bug

            self.assertEqual(finalPos[0], drawing_list[48 + j * 149].pos[0])
            self.assertEqual(finalPos[1], drawing_list[48 + j * 149].pos[1])

            # shrink the circle in 50 steps
            for i in range(0,50):
                calibPoint = drawing_list[49 + i + j * 149]
                self.assertTrue(isinstance(calibPoint, pvm.Circle))
                # size
                self.assertAlmostEqual(50 - (i + 1) * 0.9, calibPoint.radius)
                # pos
                self.assertAlmostEqual(finalPos[0], calibPoint.pos[0], delta = 10.0)
                self.assertAlmostEqual(finalPos[1], calibPoint.pos[1], delta = 13.0)
                # color
                self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
                self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

            # return point to the original size in 50 steps
            for i in range(0,50):
                calibPoint = drawing_list[99 + i + j * 149]
                self.assertTrue(isinstance(calibPoint, pvm.Circle))
                # size
                self.assertAlmostEqual(5 + (i + 1) * 0.9, calibPoint.radius)
                # pos
                self.assertAlmostEqual(finalPos[0], calibPoint.pos[0], delta = 10.0)
                self.assertAlmostEqual(finalPos[1], calibPoint.pos[1], delta = 13.0)
                # color
                self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
                self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

    def testFirstPointOnBottomRight(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)
        self.pointList = [(0.9, 0.9), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.1, 0.1)]

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])
        tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 149, len(drawing_list))

        # first 49 frame is about moving the circle to the next calib point
        for i in range(0, 49):
            calibPoint = drawing_list[i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertEqual(50, calibPoint.radius)
            # pos
            self.assertAlmostEqual(-524 + i * 22, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(294 - i * 12, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

    def testFirstPointOnBottomLeft(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)
        self.pointList = [(0.1, 0.9), (0.9, 0.1), (0.5, 0.5), (0.1, 0.1), (0.9, 0.9)]

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])
        tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 149, len(drawing_list))

        # first 49 frame is about moving the circle to the next calib point
        for i in range(0, 49):
            calibPoint = drawing_list[i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertEqual(50, calibPoint.radius)
            # pos
            self.assertAlmostEqual(524 - i * 22, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(-307, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

    def testFirstPointOnTopRight(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)
        self.pointList = [(0.9, 0.1), (0.1, 0.9), (0.5, 0.5), (0.1, 0.1), (0.9, 0.9)]

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])
        tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 149, len(drawing_list))

        # first 49 frame is about moving the circle to the next calib point
        for i in range(0, 49):
            calibPoint = drawing_list[i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertEqual(50, calibPoint.radius)
            # pos
            self.assertAlmostEqual(546, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(-294 + i * 12, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

    def testFirstPointOnCenter(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)
        self.pointList = [(0.5, 0.5), (0.9, 0.1), (0.1, 0.9), (0.1, 0.1), (0.9, 0.9)]

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])
        tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        drawing_list = visual_mock.getListOfDrawings()

        self.assertEqual(5 * 149, len(drawing_list))

        # first 49 frame is about moving the circle to the next calib point
        for i in range(0, 49):
            calibPoint = drawing_list[i]
            self.assertTrue(isinstance(calibPoint, pvm.Circle))
            # size
            self.assertEqual(50, calibPoint.radius)
            # pos
            self.assertAlmostEqual(535 - i * 11, calibPoint.pos[0], delta = 10.0)
            self.assertAlmostEqual(-294 + i * 6, calibPoint.pos[1], delta = 13.0)
            # color
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.fillColor.tolist())
            self.assertEqual([1.0, -1.0, -1.0], calibPoint.lineColor.tolist())

    def testNoReturnedValues(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['x'])

        result = tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)
        self.assertEqual(0, len(result))

    def testQuitByQ(self):
        tobii_helper = wrapper.TobiiHelper()
        self.initAll(tobii_helper)

        visual_mock = pvm.PsychoPyVisualMock()
        visual_mock.setReturnKeyList(['q'])

        with self.assertRaises(SystemExit):
            tobii_helper._TobiiHelper__getCalibrationData(self.calibWin, self.pointList)

if __name__ == "__main__":
    unittest.main() # run all tests