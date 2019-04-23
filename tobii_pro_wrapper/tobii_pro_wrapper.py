# -*- coding: utf-8 -*-

# Psychopy supported Tobii controller for the new Pro SDK

# Authors:
# Olivia Guayasamin (oguayasa@gmail.com) - Initial work as tobii-pro-wrapper (https://github.com/oguayasa/tobii_pro_wrapper)
# Tamás Zolnai (zolnaitamas2000@gmail.com) - Reworked this module.

# License: Apache License 2.0, see LICENSE.txt for more details.

# Summary: Currently provides all functionality for running a FULL CALIBRATION 
# ROUTINE for 5 and 9 point calibrations, and converting between Tobii
# Trackbox, Tobii Active Display Area, and Psychopy coordinate systems.

# Notes: This code is currently designed for working with a tobii eyetracker 
# installed on the same device as the one for running experiments (laptop set-
# up with a single connected eyetracker, no external monitors, and no tobii 
# external processors). It should be straightforward to adapt to other 
# computer/monitor set-ups, but adaptation is required. Created on Windows OS.
# Not guaranteed. 

# Please contact for questions. This will be updated as more functionality is
# added. 

# -----Import Required Libraries-----
import pyglet
from psychopy import core as pcore
from psychopy import monitors, visual, gui, data, event
from psychopy.iohub import launchHubServer

import datetime as dt
import numpy as np
from scipy.spatial import distance
import numbers

import tobii_research as tobii

import collections

# -----Class for working with Tobii Eyetrackers -----
class TobiiHelper:
    
    def __init__(self):
        
        self.eyetracker = None
        
        self.adaCoordinates = None
        
        self.tbCoordinates = None
        
        self.calibration = None
        
        self.tracking = False
        
        self.win = None
                
        self.monitorName = None

        self.gazeData = None
          
# ----- Functions for initialzing the eyetracker and class attributes -----      
    
    # find and connect to a tobii eyetracker
    def setEyeTracker(self, serialString = None):

        # if serial number is not given as a string
        if serialString is not None and not isinstance(serialString, str):
            raise TypeError("Serial number must be formatted as a string.")

        # try to find all eyetrackers
        # Sometimes the eyetracker is not identified for the first time. Try more times.
        loopCount = 1
        allTrackers = tobii.find_all_eyetrackers()
        while not allTrackers and loopCount < 10:
            allTrackers = tobii.find_all_eyetrackers()
            pcore.wait(0.01)
            loopCount += 1

        # if there are no eyetrackers
        if len(allTrackers) < 1:
            raise ValueError("Cannot find any eyetrackers.")

        # if there is no serialString specified, use first found eyetracker
        if serialString is None:
            # use first found eyetracker
            eyetracker = allTrackers[0]
            print("Address: " + eyetracker.address)
            print("Model: " + eyetracker.model)
            print("Name: " + eyetracker.device_name)
            print("Serial number: " + eyetracker.serial_number)
            # create eyetracker object
            self.eyetracker = eyetracker
        # if serial number is given as a string
        else:
            # get information about available eyetrackers
            for eyetracker in allTrackers:
                if eyetracker.serial_number == serialString:
                    print("Address: " + eyetracker.address)
                    print("Model: " + eyetracker.model)
                    # fine if name is empty
                    print("Name: " + eyetracker.device_name)
                    print("Serial number: " + eyetracker.serial_number)

                    # create eyetracker object
                    self.eyetracker = eyetracker

        # check to see that eyetracker is connected
        if self.eyetracker is None:
            raise ValueError("Eyetracker did not connect. Check serial number?")
        else:
            print("Eyetracker connected successfully.")

        # get track box and active display area coordinates
        self.__getTrackerSpace()
    
        
    # function for getting trackbox (tb) and active display area (ada)coordinates, returns
    # coordintes in two separate dictionaries with values in mm
    def __getTrackerSpace(self):
        
        # check to see that eyetracker is connected
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
            
        # get active display area information in mm as a dictionary
        displayArea = self.eyetracker.get_display_area()
        self.adaCoordinates = {}
        self.adaCoordinates['bottomLeft'] = displayArea.bottom_left
        self.adaCoordinates['bottomRight'] = displayArea.bottom_right
        self.adaCoordinates['topLeft'] = displayArea.top_left
        self.adaCoordinates['topRight'] = displayArea.top_right
        self.adaCoordinates['height'] = displayArea.height
        self.adaCoordinates['width'] = displayArea.width
    
        # get track box information in mm, return only the 2d coordinates
        # of the cube side closest to the eyetracker
        trackBox = self.eyetracker.get_track_box()
        self.tbCoordinates = {}
        self.tbCoordinates['bottomLeft'] = trackBox.front_lower_left
        self.tbCoordinates['bottomRight'] = trackBox.front_lower_right
        self.tbCoordinates['topLeft'] = trackBox.front_upper_left
        self.tbCoordinates['topRight'] = trackBox.front_upper_right
        # calculate box height and width
        trackBoxHeight = np.absolute(trackBox.front_lower_left[1] - 
                                     trackBox.front_upper_right[1])
        trackBoxWidth = np.absolute(trackBox.front_lower_left[0] - 
                                    trackBox.front_lower_right[0])
        self.tbCoordinates['height'] = trackBoxHeight
        self.tbCoordinates['width'] = trackBoxWidth

        self.tbCoordinates['frontDistance'] = trackBox.front_lower_left[2]
        self.tbCoordinates['backDistance'] = trackBox.back_lower_left[2]


    # define and calibrate experimental monitor, set monitor dimensions
    def setMonitor(self, nameString = None, dimensions = None):
        
        # find all connected monitors
        allMonitors = monitors.getAllMonitors()
        if len(allMonitors) is 0:
            raise RuntimeError("Can't find any monitor.")
            
        # if no dimensions given
        if dimensions is None:
            # use current screen dimensions
            screen = pyglet.window.get_platform().get_default_display().get_default_screen()
            dimensions = (screen.width, screen.height)
            print ("Current screen size is: " + str(dimensions[0]) + "x" + str(dimensions[1]))
        # if dimension not given as tuple
        elif not isinstance(dimensions, tuple):
            raise TypeError("Dimensions must be given as tuple.")
        elif len(dimensions) is not 2:
            raise TypeError("Dimensions must be a pair of the screen height and width.")
        elif not isinstance(dimensions[0], numbers.Number) or not isinstance(dimensions[1], numbers.Number):
            raise TypeError("The given dimensions tupple should contain numbers.")
        elif dimensions[0] <= 0 or dimensions[1] <= 0:
            raise ValueError("Screen width and height must be positive values.")
              
        # if there is not monitor name defined, go to first default monitor
        if nameString is None:
            # create monitor calibration object 
            self.monitorName = allMonitors[0]
            thisMon = monitors.Monitor(self.monitorName)
            print ("Current monitor name is: " + self.monitorName)
            # set monitor dimensions
            thisMon.setSizePix(dimensions)              
            # save monitor
            thisMon.saveMon()  # save monitor calibration
            self.win = thisMon
        # if serial number is not given as a string
        elif not isinstance(nameString, str):
            raise TypeError("Monitor name must be formatted as a string.")            
        # if serial number is given as a string
        else:
            # create monitor calibration object 
            thisMon = monitors.Monitor(nameString)
            print ("Current monitor name is: " + nameString)
            self.monitorName = nameString
            # set monitor dimensions
            thisMon.setSizePix(dimensions)              
            # save monitor
            thisMon.saveMon()  # save monitor calibration
            self.win = thisMon
                         
    def getMonitorName(self):
        if self.monitorName is None:
            raise ValueError("No monitor was set.")
        return self.monitorName

    def getMonitorDimensions(self):
        if self.win is None:
            raise ValueError("No monitor was set.")
        return (self.win.getSizePix()[0], self.win.getSizePix()[1])

# ----- Functions for starting and stopping eyetracker data collection -----

    # function for broadcasting real time gaze data
    def __gazeDataCallback(self, gazeData):
        self.gazeData = gazeData
    
    
    # function for subscribing to real time gaze data from eyetracker
    def __startGazeData(self):
       
        # check to see if eyetracker is there
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
        
        # if it is, proceed
        print ("Subscribing to eyetracker.")
        self.eyetracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA, 
                                     self.__gazeDataCallback, 
                                     as_dictionary = True)
        self.tracking = True
    
    
    # function for unsubscring from gaze data
    def __stopGazeData(self):
        
        # check to see if eyetracker is there
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
        # if it is, proceed
        print ("Unsubscribing from eyetracker")
        self.eyetracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, 
                                         self.__gazeDataCallback)
        self.tracking = False
    
        
    # function for converting normalized positions from trackbox coordinate system
    # to normalized active display area coordinates
    def __tb2Ada(self, xyCoor):
        
        # check argument values
        if not isinstance(xyCoor, tuple):
            raise TypeError("XY coordinates must be given as tuple.")
        elif len(xyCoor) is not 2:
            raise ValueError("Wrong number of coordinate dimensions.")
        elif xyCoor[0] > 1.0 or xyCoor[0] < 0.0 or xyCoor[1] > 1.0 or xyCoor[1] < 0.0:
            raise ValueError("The given coordinates should be in normalized form ([0.0,1.0]).")
        # check tracker box and ada coordinates
        if self.tbCoordinates is None or self.adaCoordinates is None:
            raise ValueError("Missing trackbox coordinates. \n" +\
                             "Try running getTrackerSpace()!")

        # get tb and ada values from eyetracker        
        tbDict = self.tbCoordinates
        adaDict = self.adaCoordinates

        # create ratios for x and y coordinates
        yRatio = tbDict.get('height')/adaDict.get('height')
        xRatio = tbDict.get('width')/adaDict.get('width')
       
        # convert and return coordinates
        adaNorm = (xyCoor[0] * xRatio, xyCoor[1] * yRatio)
        return adaNorm
    
    
    # function for converting normalized positions from trackbox coordinate system
    # to normalized coordinates based on the psychopy window
    def __tb2PsychoNorm(self, xyCoor):
        
        # check argument values
        if not isinstance(xyCoor, tuple):
            raise TypeError("XY coordinates must be given as tuple.")
        elif len(xyCoor) is not 2:
            raise ValueError("Wrong number of coordinate dimensions.")
        elif xyCoor[0] > 1.0 or xyCoor[0] < 0.0 or xyCoor[1] > 1.0 or xyCoor[1] < 0.0:
            raise ValueError("The given coordinates should be in normalized form ([0.0,1.0]).")

        # convert track box coordinates to ada coordinates
        adaCoors = self.__tb2Ada(xyCoor)
        # correct for psychopy window coordinates
        centerScale = self.__tb2Ada((1, 1))
        centerShift = (centerScale[0] / 2, centerScale[1] / 2)
        psychoNorm = (adaCoors[0] - centerShift[0], 
                      -(adaCoors[1] - centerShift[1]))
        # return coordinates in psychowin 'norm' units
        return psychoNorm
    
    
    # function for converting from tobiis ada coordinate system in normalized 
    # coordinates where (0,0) is the upper left corner, to psychopy window 
    # coordinates in pix, where (0,0) is at the center of psychopy window.
    def __ada2PsychoPix(self, xyCoor):
        
        if self.win is None:
            raise ValueError("No monitor was set.")

        # check argument values
        if not isinstance(xyCoor, tuple):
            raise TypeError("XY coordinates must be given as tuple.")
        elif len(xyCoor) is not 2:
            raise ValueError("Wrong number of coordinate dimensions.")
        elif not isinstance(xyCoor[0], numbers.Number) or not isinstance(xyCoor[1], numbers.Number):
            raise TypeError("XY coordinates must be given as number values.")
        elif xyCoor[0] > 1.0 or xyCoor[0] < 0.0 or xyCoor[1] > 1.0 or xyCoor[1] < 0.0:
            raise ValueError("The given coordinates should be in normalized form ([0.0,1.0]).")

        # convert to pixels and correct for psychopy window coordinates
        monHW = (self.win.getSizePix()[0], 
                 self.win.getSizePix()[1])
        wShift, hShift = monHW[0] / 2 , monHW[1] / 2
        psychoPix = (int((xyCoor[0]* monHW[0]) - wShift),
                     int(((xyCoor[1] * monHW[1]) - hShift) * -1))
        # return coordinates in psychowin 'pix' units
        return psychoPix

# ----- Functions for collecting eye and gaze data -----
      
    # function for collecting gaze coordinates in tobiis ada coordinate 
    # system. currently written to return the average (x, y) position of both 
    # eyes, but can be easily rewritten to return data from one or both eyes   
    def __getAvgGazePos(self):
        
        # check to see if the eyetracker is connected and turned on
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
        if self.tracking is False:
            raise ValueError("The eyetracker is not turned on.")
        if self.gazeData is None:
            raise ValueError("No recorded gaze data was found.")
            
        # access gaze data dictionary to get gaze position tuples
        leftGazeXYZ = self.gazeData['left_gaze_point_on_display_area']
        rightGazeXYZ = self.gazeData['right_gaze_point_on_display_area']
        # get 2D gaze positions for left and right eye
        xs = (leftGazeXYZ[0], rightGazeXYZ[0])
        ys = (leftGazeXYZ[1], rightGazeXYZ[1])

        # if all of the axes have data from at least one eye
        if all([np.isnan(x) for x in xs]) or all([np.isnan(y) for y in ys]):
            # take x and y averages
            avgGazePos = (np.nan, np.nan)
        else:
            # or if no data, hide points by showing off screen
            avgGazePos = (np.nanmean(xs), np.nanmean(ys))
        return avgGazePos

                
    # function for finding the avg 3d position of subject's eyes, so that they
    # can be drawn in the virtual track box before calibration. The x and y 
    # coordinates are returned in normalized "tobii track box" units.
    def __trackboxEyePos(self):
        
        # check to see if the eyetracker is connected and turned on
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
        if self.tracking is False:
            raise ValueError("The eyetracker is not turned on.")
        if self.gazeData is None:
            raise ValueError("No recorded gaze data was found.")

        # access gaze data dictionary to get eye position tuples,
        # in trackbox coordinate system
        lelfTbXYZ = self.gazeData['left_gaze_origin_in_trackbox_coordinate_system']
        rightTbXYZ = self.gazeData['right_gaze_origin_in_trackbox_coordinate_system']

        # left eye validity
        leftVal = self.gazeData['left_gaze_origin_validity']
        # right eye validity
        rightVal = self.gazeData['right_gaze_origin_validity']

        # if left eye is found by the eyetracker
        if leftVal:
            # update the left eye positions if the values are reasonable
            # scale left eye position so that it fits in track box
            leftTbPos = (-self.__tb2PsychoNorm((lelfTbXYZ[0],
                                              lelfTbXYZ[1]))[0] * 1.7,
                          self.__tb2PsychoNorm((lelfTbXYZ[0],
                                              lelfTbXYZ[1]))[1])
        else:
            # hide by drawing in the corner
            leftTbPos = [0.99, 0.99]

        # if right eye is found by the eyetracker
        if rightVal:
            # update the right eye positions if the values are reasonable
            # scale right eye position so that it fits in track box
            rightTbPos = (-self.__tb2PsychoNorm((rightTbXYZ[0], rightTbXYZ[1]))[0] * 1.7,
                           self.__tb2PsychoNorm((rightTbXYZ[0],
                                               rightTbXYZ[1]))[1])
        else:
            # hide by drawing in the corner
            rightTbPos = [0.99, 0.99]
        # return values for positio in track box
        return leftTbPos, rightTbPos
             
    
    # x, y, and z dimensions are given in mm from the tracker origin, gives the
    # average 3d position of both eyes, but can be easily rewritten to yield
    # the position of each eye separately
    def __getAvgEyePos(self):
        
        # check to see if the eyetracker is connected and turned on
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
        if self.tracking is False:
            raise ValueError("The eyetracker is not turned on.")
        if self.gazeData is None:
            raise ValueError("No recorded gaze data was found.")

        # access gaze data dictionary to get eye position tuples, given in
        # mm in from eyetracker origin
        leftOriginXYZ = self.gazeData['left_gaze_origin_in_user_coordinate_system']
        rightOriginXYZ = self.gazeData['right_gaze_origin_in_user_coordinate_system']
            
        # create arrays with positions of both eyes on x, y, and z axes
        xs = (leftOriginXYZ[0],rightOriginXYZ[0])
        ys = (leftOriginXYZ[1],rightOriginXYZ[1])
        zs = (leftOriginXYZ[2],rightOriginXYZ[2])

        # if all of the axes have data from at least one eye
        if not (np.isnan(xs)).all() and not (np.isnan(ys)).all() and not (np.isnan(zs)).all():
            # update the distance if the values are reasonable
            avgEyePos = (np.nanmean(xs), np.nanmean(ys), np.nanmean(zs))
        else:
            # otherwise set to zero
            avgEyePos = (0, 0, 0)
        # return average eye position in mm
        return avgEyePos
            
            
    # get average distance of the eyes from the tracker's plane, given in mm
    def __getAvgEyeDist(self):
        
        # check to see if the eyetracker is connected and turned on
        if self.eyetracker is None:
            raise ValueError("There is no eyetracker.")
        if self.tracking is False:
            raise ValueError("The eyetracker is not turned on.")
        if self.gazeData is None:
            raise ValueError("No recorded gaze data was found.")

        return self.__getAvgEyePos()[2]

# ----- Functions for running calibration -----
    
    # function for drawing representation of the eyes in virtual trackbox
    def __drawEyePositions(self, psychoWin):
        
        # check that psychopy window exists
        if psychoWin is None:
            raise ValueError("There is no psychopy window available. " +\
                             "Try calling runTrackbox() instead.")

        # Set default colors
        correctColor = [-1.0, 1.0, -1.0]   
        mediumColor = [1.0, 1.0, 0.0]
        wrongColor = [1.0, -1.0, -1.0]
        
        # rectangle for viewing eyes
        rectScale = self.__tb2Ada((1, 1))
        eyeArea = visual.Rect(psychoWin,
                              fillColor = [0.0, 0.0, 0.0],
                              lineColor = [0.0, 0.0, 0.0],
                              pos = [0.0, 0.0],
                              units = 'norm', 
                              lineWidth = 3,
                              width = rectScale[0],
                              height = rectScale[1])
         # Make stimuli for the left and right eye
        leftStim = visual.Circle(psychoWin, 
                                 fillColor = eyeArea.fillColor,
                                 units = 'norm', 
                                 radius = 0.07)
        rightStim = visual.Circle(psychoWin,
                                  fillColor = eyeArea.fillColor,
                                  units = 'norm', 
                                  radius = 0.07)
        # Make a dummy message
        findmsg = visual.TextStim(psychoWin,
                                  text = " ", 
                                  color = [1.0, 1.0, 1.0],
                                  units = 'norm',
                                  pos = [0.0, -0.65],
                                  height = 0.07)

        # while tracking 
        while True:         
            # find and update eye positions
            leftStim.pos, rightStim.pos = self.__trackboxEyePos()
            eyeDist = self.__getAvgEyeDist()
            frontDistance = self.tbCoordinates.get('frontDistance')
            backDistance = self.tbCoordinates.get('backDistance')
            
            # change color depending on distance
            if eyeDist >= frontDistance + 50 and eyeDist <= backDistance - 50:
                # correct distance
                leftStim.fillColor, leftStim.lineColor = correctColor, correctColor
                rightStim.fillColor, rightStim.lineColor = correctColor, correctColor
            elif (eyeDist < frontDistance + 50 and eyeDist > frontDistance) or (eyeDist > backDistance - 50 and eyeDist < backDistance):
                leftStim.fillColor, leftStim.lineColor = mediumColor, mediumColor
                rightStim.fillColor, rightStim.lineColor = mediumColor, mediumColor
            else:
                # not really correct
                leftStim.fillColor, leftStim.lineColor = wrongColor, wrongColor
                rightStim.fillColor, rightStim.lineColor = wrongColor, wrongColor
                
            # if left eye is not found, don't display eye    
            if leftStim.pos[0] == 0.99: 
                leftStim.fillColor = psychoWin.color  # make the same color as bkg
                leftStim.lineColor = psychoWin.color
                
            # if right eye is not found, don't display eye
            if rightStim.pos[0] == 0.99:
                rightStim.fillColor = psychoWin.color  # make same color as bkg
                rightStim.lineColor = psychoWin.color    
    
            # give distance feedback
            findmsg.text = "You're currently " + \
                            str(int(eyeDist/10)) + \
                            (" cm away from the screen. \n"
                             "Press 'c' to calibrate or 'q' to abort.")
                   
            # update stimuli in window
            eyeArea.draw()
            leftStim.draw()
            rightStim.draw()
            findmsg.draw()
            psychoWin.flip()
            
            # depending on response, either abort script or continue to calibration
            if event.getKeys(keyList=['q']):
                self.__stopGazeData()
                psychoWin.close()
                pcore.quit()
            elif event.getKeys(keyList=['c']):
                print("Proceeding to calibration.")
                self.__stopGazeData()
                psychoWin.flip()
                return 
        
            # clear events not accessed this iteration
            event.clearEvents(eventType='keyboard')

    def __drawValidationScreen(self, pointDict, valWin):

        # check the values of the point dictionary
        if not isinstance(pointDict, dict):
            raise TypeError('pointDict must be a dictionary with number ' +\
                            'keys and coordinate values.')
        if not isinstance(valWin, visual.Window):
            raise TypeError('valWin should be a valid visual.Window object.')
        # check window attribute
        if self.win is None:
            raise ValueError('No experimental monitor has been specified.\n' +\
                             'Try running setMonitor().')

        # get points from dictionary
        curPoints = pointDict.values()

        # convert points from normalized ada units to psychopy pix
        pointPositions = [self.__ada2PsychoPix(x) for x in curPoints]

        # stimuli for showing point of gaze
        gazeStim = visual.Circle(valWin,
                                 radius = 50,
                                 lineColor = [1.0, 0.95, 0.0],  # yellow circle
                                 fillColor = [1.0, 1.0, 0.55],  # light interior
                                 lineWidth = 40,
                                 units = 'pix')
        # Make a dummy message
        valMsg = visual.TextStim(valWin,
                                 text = 'Wait for the experimenter.',
                                 color = [0.4, 0.4, 0.4],  # grey
                                 units = 'norm',
                                 pos = [0.0, -0.5],
                                 height = 0.07)
        # Stimuli for all validation points
        valPoints = visual.Circle(valWin,
                                  units = "pix",
                                  radius = 20,
                                  lineColor = [1.0, -1.0, -1.0],  # red
                                  fillColor = [1.0, -1.0, -1.0])  # red

        # create array for smoothing gaze position
        gazePositions = None
        maxLength = 6

        # while tracking
        while True:

            avgGazePos = self.__getAvgGazePos()
            if np.isnan(avgGazePos[0]) or np.isnan(avgGazePos[1]):
                curPos = (np.nan, np.nan)
            else:
                # smooth gaze data with moving window
                if gazePositions is None:
                    gazePositions = np.array([avgGazePos])
                else:
                    gazePositions = np.vstack((gazePositions,
                                               np.array(avgGazePos)))
                curPos = np.nanmean(gazePositions, axis = 0)

            # remove previous position values
            if gazePositions is not None and len(gazePositions) == maxLength:
                gazePositions = np.delete(gazePositions, 0, axis = 0)

            # update stimuli in window and draw if we have a valid pos
            if not np.isnan(curPos[0]) and curPos[0] <= 1.0 and curPos[0] >= 0.0 and \
               not np.isnan(curPos[1]) and curPos[1] <= 1.0 and curPos[1] >= 0.0:
                gazeStim.pos = self.__ada2PsychoPix(tuple(curPos))
                gazeStim.draw()

            # points
            for point in pointPositions:
                valPoints.pos = point
                valPoints.draw()

            # text
            valMsg.draw()
            valWin.flip()

            # depending on response, either abort script or continue to calibration
            if event.getKeys(keyList=['q']):
                self.__stopGazeData()
                pcore.quit()
            elif event.getKeys(keyList=['c']):
                print ("Exiting calibration validation.")
                self.__stopGazeData()
                return

            # clear events not accessed this iteration
            event.clearEvents(eventType='keyboard')


    # function for running validation routine post calibration to check 
    # calibration precision and accuracy
    def runValidation(self, pointDict = None, valWin = None):

        # check the values of the point dictionary
        if pointDict is None:
            print('pointDict has no value. Using 5 point default.')
            pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)), 
                         ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
            pointDict = collections.OrderedDict(pointList)
        if not isinstance(pointDict, dict):
            raise TypeError('pointDict must be a dictionary with number ' +\
                            'keys and coordinate values.')
        if valWin is not None and not isinstance(valWin, visual.Window):
            raise TypeError('valWin should be a valid visual.Window object.')
        # check window attribute
        if self.win is None:
            raise ValueError('No experimental monitor has been specified.\n' +\
                             'Try running setMonitor().')
        # start eyetracker
        self.__startGazeData()
        # let it warm up briefly
        pcore.wait(0.5)

        # use existing window
        if valWin is not None:
            self.__drawValidationScreen(pointDict, valWin)
        else:
            # window stimuli
            with visual.Window(size = [self.win.getSizePix()[0],
                                       self.win.getSizePix()[1]],
                                       pos = [0, 0],
                                       units = 'pix',
                                       fullscr = True,
                                       allowGUI = True,
                                       monitor = self.win,
                                       winType = 'pyglet',
                                       color = [0.8, 0.8, 0.8]) as ownValWin:
                self.__drawValidationScreen(pointDict, ownValWin)

            
    # function for getting the average left and right gaze position coordinates
    # for each calibration point in psychopy pix units
    def __calculateCalibration(self, calibResult):
        
        # check the values of the point dictionary
        if not isinstance(calibResult, tobii.CalibrationResult):
            raise ValueError('Argument should be a valid tobii_research.CalibResult object')
   
        #create an empty list to hold values
        calibDrawCoor = []
        
        # iterate through calibration points
        for i in range(len(calibResult.calibration_points)):
            # current point
            curPoint = calibResult.calibration_points[i]
            pointPosition = curPoint.position_on_display_area  # point position
            pointSamples = curPoint.calibration_samples  # samples at point
            # empty arrays for holding left and right eye gaze coordinates
            leftOutput = np.zeros((len(pointSamples), 2))
            rightOutput = np.zeros((len(pointSamples), 2))
            
            # find left and right gaze coordinates for all samples in point
            for j in range(len(pointSamples)):
                curSample = pointSamples[j]
                leftEye = curSample.left_eye
                rightEye = curSample.right_eye
                leftOutput[j] = leftEye.position_on_display_area
                rightOutput[j] = rightEye.position_on_display_area
                
            # get average x and y coordinates using all samples in point
            leftXY = tuple(np.mean(leftOutput, axis = 0))
            rightXY = tuple(np.mean(rightOutput, axis = 0))
            point = tuple((pointPosition[0], pointPosition[1]))
            # put current calibration point coordinates , l and r eye coordinates
            # into list, and convert to psychopy window coordinates in pix
            newList = [self.__ada2PsychoPix(point), self.__ada2PsychoPix(leftXY),
                       self.__ada2PsychoPix(rightXY), pointPosition]
            calibDrawCoor.insert(i, newList)
            
        # for some weird reason my calibration always includes the point (0,0) at 
        # index 0, so just remove it here
        calibDrawCoor.pop(0)
        # return as list
        return calibDrawCoor
       
    
    # function for drawing the results of the calibration
    def __drawCalibrationResults(self, calibResult, calibWin, curDict):
        
        # check argument values
        if self.calibration is None:
            raise ValueError('No calibration object exists.')
        # check values of calibration result
        if not isinstance(calibResult, tobii.CalibrationResult):
            raise TypeError('calibResult should be a valid tobii_research.CalibrationResult object.')
        if not isinstance(calibWin, visual.Window):
            raise TypeError('calibWin should be a visual.Window object.')
        # check the values of the point dictionary
        if not isinstance(curDict, dict):
            raise TypeError('curDict must be a dictionary with number \n' +\
                            'keys and coordinate values.')
        if len(curDict) != len(calibResult.calibration_points) - 1: # TODO: why it this minus 1 is here
            raise ValueError('Data inconsistency: calibResult and curDict have different amount of items')

        # get gaze position results
        points2Draw = self.__calculateCalibration(calibResult)
        
        # create stimuli objects for drawing
        # outlined empty circle object for showing calibration point
        calibPoint = visual.Circle(calibWin, 
                                   radius = 50,
                                   lineColor = [1.0, 1.0, 1.0],  # white
                                   lineWidth = 10,
                                   fillColor = calibWin.color,
                                   units = 'pix',
                                   pos = (0.0, 0.0))  
        # line object for showing right eye gaze position during calibration 
        rightEyeLine = visual.Line(calibWin, 
                                   units ='pix',
                                   lineColor ='red',
                                   lineWidth = 20,
                                   start = (0.0, 0.0),
                                   end = (0.0, 0.0))                              
        # line object for showing left eye gaze position during calibration                          
        leftEyeLine = visual.Line(calibWin, 
                                  units ='pix',
                                  lineColor ='yellow',
                                  lineWidth = 20,
                                  start = (0.0, 0.0),
                                  end = (0.0, 0.0))
        # number for identifying point in dictionary
        pointText = visual.TextStim(calibWin, 
                                    text = " ", 
                                    color = [0.8, 0.8, 0.8],  # lighter than bkg
                                    units = 'pix',
                                    pos = [0.0, 0.0],
                                    height = 60)
        # Make a dummy message
        checkMsg = visual.TextStim(calibWin,
                                   text = 'Wait for the experimenter.',
                                   color = [1.0, 1.0, 1.0],
                                   units = 'norm',
                                   pos = [0.0, -0.5],
                                   height = 0.07)

        # make empty dictionary for holding points to be recalibrated
        holdRedoDict = []
        holdColorPoints = []
        
        # clear events not accessed this iteration
        event.clearEvents(eventType='keyboard')   
    
        # draw and update screen
        while True: 
          
            # iterate through calibration points and draw
            for i in range(len(points2Draw)):
                # update point and calibraiton results for both eyes
                point = points2Draw[i] 
                pointPos = point[3]
                pointKey = 0
                
                # update text
                pointFound = False
                for key, point in curDict.items():
                    if point == pointPos:
                        pointText.text = key
                        pointKey = key
                        pointFound = True

                if not pointFound:
                    raise ValueError('Data inconsistency: calibResult and curDict contains different items.')

                # if current point is selected for recalibrate, make it noticeable
                if int(pointKey) in holdColorPoints:
                    calibPoint.lineColor = [-1.0, 1.0, -1.0]  # green circle
                else:
                    calibPoint.lineColor = [1.0, 1.0, 1.0]  # no visible change
                    
                # update point and calibraiton results for both eyes
                point = points2Draw[i]   
                startCoor, leftCoor, rightCoor = point[0], point[1], point[2]
                # update positions and draw  on window
                calibPoint.pos = startCoor  # calibration point
                leftEyeLine.start = startCoor  # left eye
                leftEyeLine.end = leftCoor
                rightEyeLine.start = startCoor  # right eye
                rightEyeLine.end = rightCoor
                pointText.pos = startCoor  # point text
                
                # update stimuli in window
                calibPoint.draw()  # has to come first or else will cover other
                # stim
                pointText.draw() 
                leftEyeLine.draw()
                rightEyeLine.draw()

            checkMsg.draw()
            
            # show points and lines on window         
            calibWin.flip()
            
            keyList = ['c', 'q']
            for key, point in curDict.items():
                keyList.append(key)

            pressedKeys = event.getKeys(keyList)

            # depending on response, either...
            # abort script
            for key in pressedKeys:
                if key in ['q']:
                    calibWin.close()
                    self.calibration.leave_calibration_mode()
                    pcore.quit()
                
                # else if recalibration point is requested
                elif key in curDict.keys():
                    # iterate through each of these presses
                    for entry in curDict.items():
                        # if the key press is the same as the current dictionary key
                        if entry[0] == key:
                            # append that dictionary entry into a holding dictionary
                            holdRedoDict.append(entry)
                            # append integer version to a holding list  
                            holdColorPoints.append(int(key))
                                
                # continue with calibration procedure           
                elif key in ['c']:
                    print ("Finished checking. Resuming calibration.")
                    checkMsg.pos = (0.0, 0.0)
                    checkMsg.text = ("Finished checking. Resuming calibration.")
                    checkMsg.draw()
                    calibWin.flip() 
    
                    # return dictionary of points to be recalibration
                    redoDict = collections.OrderedDict([])  # empty dictionary for holding unique values
                    # dont put repeats in resulting dictionary
                    tempDict = collections.OrderedDict(holdRedoDict)
                    for keys in tempDict.keys():
                        if keys not in redoDict.keys():
                            redoDict[keys] = tempDict.get(keys)
    
                    # return dictionary
                    return redoDict
                        
            # clear events not accessed this iteration
            event.clearEvents(eventType='keyboard')


    # function for drawing calibration points, collecting and applying 
    # calibration data
    def __getCalibrationData(self, calibWin, pointList):
        
        # check argument values
        if self.calibration is None:
            raise ValueError('No calibration object exists')
        # check value of calibration window
        if not isinstance(calibWin, visual.Window):
            raise TypeError('calibWin should be a visual.Window object.')
        # check the values of the point dictionary
        if not isinstance(pointList, list):
            raise TypeError('pointList must be a list of coordinate tuples.')

        # defaults
        pointSmallRadius = 5.0  # point radius
        pointLargeRadius = pointSmallRadius * 10.0  
        moveFrames = 50 # number of frames to draw between points
        startPoint = pointList[-1] # starter point for animation
    
        # calibraiton point visual object
        calibPoint = visual.Circle(calibWin, 
                                   radius = pointLargeRadius,
                                   lineColor = [1.0, -1.0, -1.0],  # red
                                   fillColor = [1.0, -1.0, -1.0],
                                   units = 'pix')

        # draw animation for each point
        # converting psychopy window coordinate units from normal to px
        for i in range(len(pointList)):    
            
            # if first point draw starting point
            if i == 0:
                firstPoint = [startPoint[0], startPoint[1]]
                secondPoint = [pointList[i][0], pointList[i][1]]
            else:
                firstPoint = [pointList[i - 1][0], pointList[i - 1][1]]
                secondPoint = [pointList[i][0], pointList[i][1]]
                   
            # draw and move dot
            # step size for dot movement is new - old divided by frames
            pointStep = [(secondPoint[0] - firstPoint[0]) / moveFrames,
                         (secondPoint[1] - firstPoint[1]) / moveFrames]
            
            # Move the point in position (smooth pursuit)
            for frame in range(moveFrames):
                firstPoint[0] += pointStep[0]
                firstPoint[1] += pointStep[1]
                # draw & flip
                calibPoint.pos = self.__ada2PsychoPix(tuple(firstPoint))
                calibPoint.draw()
                calibWin.flip()          
            # wait to let eyes settle    
            pcore.wait(0.5)    
            
            # allow the eye to focus before beginning calibration
            # point size change step
            radiusStep = ((pointLargeRadius - pointSmallRadius) / moveFrames)
            
            # Shrink the outer point (gaze fixation) to encourage focusing
            for frame in range(moveFrames):
                pointLargeRadius -= radiusStep
                calibPoint.radius = pointLargeRadius
                calibPoint.draw()
                calibWin.flip()    
            # first wait to let the eyes settle 
            pcore.wait(0.5)  
            
            # conduct calibration of point
            print ("Collecting data at {0}." .format(i + 1))
            while self.calibration.collect_data(pointList[i][0], 
                                                pointList[i][1]) != tobii.CALIBRATION_STATUS_SUCCESS:
                self.calibration.collect_data(pointList[i][0], 
                                              pointList[i][1])   
                
            # feedback from calibration
            print ("{0} for data at point {1}." 
                   .format(self.calibration.collect_data(pointList[i][0],
                   pointList[i][1]), i + 1))
            pcore.wait(0.3)  # wait before continuing
          
            # Return point to original size
            for frame in range(moveFrames):
                pointLargeRadius += radiusStep
                calibPoint.radius = pointLargeRadius
                calibPoint.draw()
                calibWin.flip()      
            # let the eyes settle and move to the next point 
            pcore.wait(0.2)      
              
            # check to quit  
            # depending on response, either abort script or continue to calibration
            if event.getKeys(keyList=['q']):
                calibWin.close()
                self.calibration.leave_calibration_mode()
                pcore.quit()
                return
                
            # clear events not accessed this iteration
            event.clearEvents(eventType='keyboard')
        
        # clear screen
        calibWin.flip()   
        # print feedback
        print ("Computing and applying calibration.")
        # compute and apply calibration to get calibration result object    
        calibResult = self.calibration.compute_and_apply()        
        # return calibration result
        return calibResult
    
    
    # function for running simple gui to visualize subject eye position. Make 
    # sure that the eyes are in optimal location for eye tracker
    def runTrackBox(self, trackWin = None):
        
        # check to see that eyetracker is connected
        if self.eyetracker is None:
            raise ValueError('There is no eyetracker object. \n' +\
                             'Try running findTracker().')
        # check window attribute
        if self.win is None:
            raise ValueError('No experimental monitor has been specified.\n' +\
                             'Try running setMonitor().')
        if trackWin is not None and not isinstance(trackWin, visual.Window):
            raise TypeError('If trackWin parameter is set, then it should be valid visual.Window object')

        # start the eyetracker
        self.__startGazeData()
        # wait for it ot warm up
        pcore.wait(0.5)

        # use the existing window
        if trackWin is not None:
            # feedback about eye position
            self.__drawEyePositions(trackWin)
            pcore.wait(2)
        else: # use an own window
            # create window for visualizing eye position and text
            with visual.Window(size = [self.win.getSizePix()[0],
                                       self.win.getSizePix()[1]],
                                       pos = [0, 0],
                                       units = 'pix',
                                       fullscr = True,
                                       allowGUI = True,
                                       monitor = self.win,
                                       winType = 'pyglet',
                                       color = [0.4, 0.4, 0.4]) as ownTrackWin:

                # feedback about eye position
                self.__drawEyePositions(ownTrackWin)
                pcore.wait(2)

        return

    def __drawCalibrationScreen(self, calibDict, calibWin):

        # check the values of the point dictionary
        if not isinstance(calibDict, dict):
            raise TypeError('calibDict must be a dictionary with number ' +\
                            'keys and coordinate values.')
        if not isinstance(calibWin, visual.Window):
            raise TypeError('calibWin should be a valid visual.Window object.')

        # stimuli for holding text
        calibMessage = visual.TextStim(calibWin, 
                                       color = [1.0, 1.0, 1.0],  # text
                                       units = 'norm', 
                                       height = 0.08, 
                                       pos = (0.0, 0.1))
        # stimuli for fixation cross
        fixCross = visual.TextStim(calibWin,
                                   color = [1.0, 1.0, 1.0],
                                   units = 'norm', 
                                   height = 0.1, 
                                   pos = (0.0, 0.0),
                                   text = "+")
       
        # initialize calibration
        self.calibration = tobii.ScreenBasedCalibration(self.eyetracker)  # calib object 
        # enter calibration mode
        self.calibration.enter_calibration_mode()
        # subject instructions
        calibMessage.text = ("Please focus your eyes on the red dot " + \
                             "and follow it with your eyes as closely as " + \
                             "possible.\n\nPress 'c' to continue.")
        calibMessage.draw()
        calibWin.flip()   
            
        # turn keyboard reporting on and get subject response
        event.waitKeys(maxWait = 10, keyList = ['c'])  # proceed with calibration
    
        # draw a fixation cross
        fixCross.draw()
        calibWin.flip()
        pcore.wait(3)
        
        # create dictionary for holding points to be recalibrated
        redoCalDict = calibDict
        
        # loop through calibration process until calibration is complete
        while True:
            
            # create point order form randomized dictionary values
            pointOrder = list(redoCalDict.values())
            # perform calibration 
            calibResult = self.__getCalibrationData(calibWin, pointOrder)
    
            # Check status of calibration result
            # if calibration was successful, check calibration results
            if calibResult.status != tobii.CALIBRATION_STATUS_FAILURE: # TODO: what if only one eye failes
                # give feedback
                calibMessage.text = ("Applying calibration...")
                calibMessage.draw()
                calibWin.flip()
                pcore.wait(2)
                # moving on to accuracy plot
                calibMessage.text = ("Calculating calibration accuracy...")
                calibMessage.draw()
                calibWin.flip()
                pcore.wait(2)
                
                # check calibration for poorly calibrated points
                redoCalDict = self.__drawCalibrationResults(calibResult, 
                                                          calibWin, 
                                                          calibDict)
       
            else:  # if calibration was not successful, leave and abort
                calibMessage.text = ("Calibration was not successful.\n\n" + \
                                     "Closing the calibration window.")
                calibMessage.draw()
                calibWin.flip()
                pcore.wait(3)
                calibWin.close()
                self.calibration.leave_calibration_mode()
                return
                    
            # Redo calibration for specific points if necessary 
            if not redoCalDict:  # if no points to redo
            # finish calibration
                print ("Calibration successful. Moving on to validation mode.")
                calibMessage.text = ("Calibration was successful.\n\n" + \
                                     "Moving on to validation.")
                calibMessage.draw()
                calibWin.flip()
                pcore.wait(3)
                self.calibration.leave_calibration_mode()
                # break loop to proceed with validation
                break
            
            else:  # if any points to redo
                # convert list to string for feedback
                printString = " ".join(str(x) for x in redoCalDict.keys())
                # feedback
                print ("Still need to calibrate the following points: %s" 
                       % printString)
                calibMessage.text = ("Calibration is almost complete.\n\n" + \
                                 "Prepare to recalibrate a few points.")
                calibMessage.draw()
                calibWin.flip()
                pcore.wait(3)
                # draw fixation cross
                fixCross.draw()
                calibWin.flip()
                pcore.wait(3)
                
                # iterate through list of redo points and remove data from calibration
                for newPoint in redoCalDict.values():
                    print (newPoint)
                    self.calibration.discard_data(newPoint[0], newPoint[1])
            
        # Validate calibration
        # draw fixation cross
        fixCross.draw()
        calibWin.flip()
        pcore.wait(3)


    # function for running a complete calibration routine
    def runFullCalibration(self, numCalibPoints = None):

        if numCalibPoints is not None:
            if not isinstance(numCalibPoints, numbers.Number):
                raise TypeError("numCalibPoints should be a number.")
            if numCalibPoints not in [5, 9]:
                raise ValueError("Only 5 or 9 points calibration is supported.")

        # check that eyetracker is connected before running
        if self.eyetracker is None:  # eyeTracker
            raise ValueError("No eyetracker is specified. " +\
                             "Aborting calibration.\n" +\
                             "Try running findTracker().")
        # check window attribute
        if self.win is None:
            raise ValueError('No experimental monitor has been specified.\n' +\
                             'Try running setMonitor().')

        # create dictionary of calibration points
        # if nothing entered then default is five
        if numCalibPoints is None:
            pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)),
                         ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
        elif numCalibPoints is 5:
            pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)),
                         ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
        elif numCalibPoints is 9:
            pointList = [('1',(0.1, 0.1)), ('2',(0.5, 0.1)), ('3',(0.9, 0.1)),
                         ('4',(0.1, 0.5)), ('5',(0.5, 0.5)), ('6',(0.9, 0.5)),
                         ('7',(0.1, 0.9)), ('8',(0.5, 0.9)), ('9',(0.9, 0.9))]

        # randomize points as ordered dictionary
        np.random.shuffle(pointList)
        calibDict = collections.OrderedDict(pointList)

        # create window for calibration
        calibWin = visual.Window(size = [self.win.getSizePix()[0],
                                         self.win.getSizePix()[1]],
                                 pos = [0, 0],
                                 units = 'pix',
                                 fullscr = True,
                                 allowGUI = True,
                                 monitor = self.win,
                                 winType = 'pyglet',
                                 color = [0.4, 0.4, 0.4])
        # stimuli for holding text
        calibMessage = visual.TextStim(calibWin,
                                       color = [1.0, 1.0, 1.0],  # text
                                       units = 'norm',
                                       height = 0.08,
                                       pos = (0.0, 0.1))

        # track box to position participant
        # subject instructions for track box
        calibMessage.text = ("Please position yourself so that the\n" + \
                             "eye-tracker can locate your eyes." + \
                             "\n\nPress 'c' to continue.")
        calibMessage.draw()
        calibWin.flip()
        # turn keyboard reporting on and get subject response
        event.waitKeys(maxWait = 10, keyList = ['c'])  # proceed with calibration

        #run track box routine
        calibWin.flip()   # clear previous text
        self.runTrackBox(calibWin)

        # run calibration rutine
        self.__drawCalibrationScreen(calibDict, calibWin)

        # run validation
        self.runValidation(calibDict, calibWin)
        # close window
        calibMessage.text = ("Finished validating the calibration.\n\n" +\
                             "Calibration is complete. Closing window.")
        calibMessage.draw()
        calibWin.flip()
        pcore.wait(3)
        calibWin.close() 
        return
  












