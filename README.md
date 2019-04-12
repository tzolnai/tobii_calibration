# tobii-calibration

Derivetive code from tobii-pro-wrapper: https://github.com/oguayasa/. This code is work-in-progress,
if you would like to use these functionalites you can use the original wrapper code.

Contains functions for working with with the new Tobii Pro SDK for Python,
along with essential eye-tracking routines, in a TobiiHelper class.

## Getting Started

### Prerequisites
Running tobii_pro_wrapper requires all of the following and their dependencies. 

* [Python 3.5](https://www.python.org/downloads/)
* [Tobii Pro SDK](https://pypi.org/project/tobii-research/) for Python 3.5

```
pip install tobii_research
```
You will need PsychoPy for using this module. However there is no standalone PsychoPy
supporting Python 3.5, so you'll need to use the manual installation (see the link bellow).
Other dependencies bellow are also used by PsychoPy, so it's likely you'll have them after
PsychoPy is installed.

* [Psychopy](https://www.psychopy.org/installation.html#manual-install)
* [numpy](https://scipy.org/install.html)
* [scipy](https://scipy.org/install.html)
* [pyglet](https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/)

### Installing

Download or clone the whole project then go into the folder of it and call setup.py:

```
python setup.py install
```

## Package Details

### TobiiHelper() *class*
A class for a wrapper for the Tobii Pro SDK for Python. Contains the following attributes:

```
        self.eyetracker = None
        
        self.adaCoordinates = None
        
        self.tbCoordinates = None
        
        self.calibration = None
        
        self.tracking = False
        
        self.win = None
                
        self.gazeData = {}
```

### findTracker(serialString = None)
Find and connect to the eyetracker identified by its serial number.
If no serial number is given, defaults to connecting to the first eyetracker it can find.
Sets the self.eyetracker attribute.

### setMonitor(nameString = None, dimensions = None)
Creates, selects, and calibrates a psychopy.monitor object. You can select a specific
monitor with **nameString** and set its dimensions with **dimensions**. If no **nameString** or 
**dimensions** are given, it will use the default monitor and that monitors dimensions. Sets the
self.win attributes

### startGazeData()
Connect to the eyetracker and uses the **self.gazeData** attribute to
broadcast all gaze data as a dictionary.

### getGazeData()
Takes the gaze data dictionary specified by Tobii (self.gazeData), pulls out important values, and converts
those values to more readily understood measurements. 

Returns a single row (current sample) dictionary with gaze positions, eye positions,
pupil size, and eye validities. 

### stopGazeData()
Disconnect from the eyetracker and stops broadcasting gaze data.

### tb2Ada(xyCoor = tuple)
Takes trackbox location coordinates and converts to active display area coordinates. Returns an (x,y)
coordinate tuple. 

### tb2PsychoNorm(xyCoor = tuple)
Takes trackbox location coordinates and converts psychopy window normal units. Returns an (x,y)
coordinate tuple. 

### ada2MonPix(xyCoor = tuple)
Takes active display area coordinates and converts to monitor pixel coordinates. Returns an (x,y)
coordinate tuple. 

### getAvgGazePos()
Uses broadcasting **self.gazeData** to return the average (x,y) gaze position of the left and right eyes as a
tuple. Gaze position is returned in active display area units.

### getAvgEyePos()
Uses broadcasting **self.gazeData** to return the average 3D (x, y, z) physical position of the left and right 
eyes relative to the eyetracker origin as a tuple. Returns position in mm units. 

### getAvgEyeDist()
Uses broadcasting **self.gazeData** and **self.getAvgEyePos()** to return average distance of the left and right eyes
from the eyetracker origin. Retures position in cm units.

### runValidation(pointDict = dict)
Shows real time gaze position and draws several reference points (**pointDict** is a dictionary with numbered keys
and coordinate values for drawing those points) to check calibration quality. If no value for **pointDict** is given,
reference points will be drawn at the standard locations for a 5 point calibration.

### runTrackBox()
Shows real time eye position within in the Tobii eyetracker trackbox. Uses colors and reported eye distance to let
the subject know if they are well positioned relative to the tracker.

### runFullCalibration(numCalibPoints = int())
Runs a full 5 or 9 point calibration routine as specified by **numCalibPoints**. If **numCalibPoints** is not defined,
then the default is a 9 point calibration. This full calibration routine includes: finding eye positions within the trackbox,
running a calibration, showing calibration accuracy, re-calibrating problem points, checking the quality of the calibration, and
saving the calibration to the eyetracker. Requires a working keyboard to control. 

## Examples

To find the eyetracker, determing eyetracker coordinatest, define the experimental monitor, 
and run a full 5-point calibration routine:

```
# Import the wrapper
import tobii_pro_wrapper as tpw

# Create a TobiiHelper object
foo = tpw.TobiiHelper()

# Idenfity and define the experimental monitor
foo.setMonitor(nameString = None, dimensions = None)

# Find eyetrackers and connect
foo.findTracker(serialString = None)

# Run a full 5 point calibration routing
foo.runFullCalibration(numCalibPoints = 5)

```

To start, output, and stop the eyetracker's collection of gaze data:

```
# start the eyetracker
foo.startGazeData()

# to get real time gaze data, place this command within a "while" loop 
# during each trial run
foo.getCurrentData()

# stop the eyetracker
foo.stopGazeData()

```

That's it!

Further examples will be linked below as they are developed.

## Authors

**Olivia Guayasamin** - *Initial work and development* - [oguayasa](https://github.com/oguayasa)

**Tamás Zolnai** - *Reworked this module* - [tzolnai](https://github.com/tzolnai)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/tzolnai/tobii_calibration/blob/master/LICENSE.txt) file for details.



