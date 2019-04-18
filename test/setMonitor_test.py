# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

import unittest

import sys
# Add the local path of the wrapper module,
# test that instead of the system installed one.
sys.path = ["../tobii_pro_wrapper"] + sys.path

import tobii_pro_wrapper as wrapper
from psychopy import monitors
import pyglet

class setMonitorTest(unittest.TestCase):

    def testMonitorNotInited(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper.getMonitorName()            
        with self.assertRaises(ValueError):
            tobii_helper.getMonitorDimensions()

    def testNoParam(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor()
        self.assertEqual(monitors.getAllMonitors()[0], tobii_helper.getMonitorName())
        screen = pyglet.window.get_platform().get_default_display().get_default_screen();
        self.assertEqual((screen.width, screen.height), tobii_helper.getMonitorDimensions())
        
    def testWrongNameParam(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.setMonitor(nameString = (1, 2))
        
    def testCallWithMonitorName(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor(monitors.getAllMonitors()[0])
        self.assertEqual(monitors.getAllMonitors()[0], tobii_helper.getMonitorName())
        screen = pyglet.window.get_platform().get_default_display().get_default_screen();
        self.assertEqual((screen.width, screen.height), tobii_helper.getMonitorDimensions())
                
    def testCallWithNonExisitngMonitorName(self):
        tobii_helper = wrapper.TobiiHelper()
        name = monitors.getAllMonitors()[0] + monitors.getAllMonitors()[0]
        tobii_helper.setMonitor(name)
        self.assertEqual(name, tobii_helper.getMonitorName())
        screen = pyglet.window.get_platform().get_default_display().get_default_screen();
        self.assertEqual((screen.width, screen.height), tobii_helper.getMonitorDimensions())
        
    def testWrongDimensionParam(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.setMonitor(dimensions = "dim")
            
    def testWrongDimensionParam2(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.setMonitor(dimensions = ("dim", "dim2"))            
            
    def testWrongDimensionParam3(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(TypeError):
            tobii_helper.setMonitor(dimensions = (1, 2, 3))
            
    def testWrongDimensionParam4(self):
        tobii_helper = wrapper.TobiiHelper()
        with self.assertRaises(ValueError):
            tobii_helper.setMonitor(dimensions = (-100, 2))
            
    def testCallWithIntegerDimensions(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor(dimensions = (1366, 768))
        self.assertEqual(monitors.getAllMonitors()[0], tobii_helper.getMonitorName())
        self.assertEqual((1366, 768), tobii_helper.getMonitorDimensions())
            
    def testCallWithFloatDimensions(self):
        tobii_helper = wrapper.TobiiHelper()
        tobii_helper.setMonitor(dimensions = (1366.0, 768.0))
        self.assertEqual(monitors.getAllMonitors()[0], tobii_helper.getMonitorName())
        self.assertEqual((1366.0, 768.0), tobii_helper.getMonitorDimensions())


if __name__ == "__main__":
    unittest.main() # run all tests