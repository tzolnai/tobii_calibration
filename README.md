# tobii_calibration

This package contains useful rutines for calibration using a Tobii Pro SDK for Python.
Three main parts of calibration are supported:
1. Trackbox visualization to allow positioning of the subject's eye inside
the eye tracker's track box (see runTrackBox).
2. Displaying calibration points and collection calibraton data (see runFullCalibration).
3. Validation screen which can be used after calibration to validate that the eye tracker
records the eye positions correctly (see runValidation).

Derivetive code from tobii-pro-wrapper: https://github.com/oguayasa/tobii_pro_wrapper.
This code is in 'work-in-progress' state.

## Getting Started

### Prerequisites
Running tobii_calibration requires all of the following and their dependencies.

* [Python 3.5](https://www.python.org/downloads/)
* [Tobii Pro SDK](https://pypi.org/project/tobii-research/) for Python 3.5

```
pip install tobii_research
```

You will need PsychoPy for using this module. However there is no standalone PsychoPy
supporting Python 3.5, so you'll need to use the [manual installation](https://www.psychopy.org/installation.html#manual-install).
Other dependencies bellow are also used by PsychoPy, so it's likely you'll have them after
PsychoPy is installed.

* [Psychopy](https://www.psychopy.org/installation.html#manual-install)
* [numpy](https://scipy.org/install.html)
* [pyglet](https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/)

### Installing

Download or clone the whole project then go into the folder of it and call setup.py:

```
python setup.py install
```

For installing it with a non english language run the following command
(only Hungarian translation is supported by now):

```
python setup.py install --lang hu
```

## Package Details

### TobiiHelper() *class*
A class for doing calibration using the Tobii Pro SDK for Python. Contains the following functions:

### setEyeTracker(serialString = None)
Find and connect to the eyetracker identified by its serial number.
If no serial number is given, defaults to connecting to the first eyetracker it can find.
Sets the self.eyetracker attribute.

### setMonitor(nameString = None, dimensions = None)
Creates, selects, and calibrates a psychopy.monitor object. You can select a specific
monitor with **nameString** and set its dimensions with **dimensions**. If no **nameString** or
**dimensions** are given, it will use the default monitor and that monitors dimensions. Sets the
self.win attributes

### getMonitorName()
Returns the name of the selected monitor. This name comes from an earlier setMonitor() call
or get from the default monitor.

### getMonitorDimensions()
Returns the screen width and height of the selected monitor. This dimensions can be set with setMonitor
method. If it was not specified, then the code uses the default screen size.

### enableLogging()
Enables logging messages printed to the command line (enabled by default).

### disableLogging()
Disables logging messages printed to the command line (enabled by default).

### setAccuracy(accuracyInPixel)
Sets the used accuracy in pixel unit. This accuracy value is used during calibration to draw the acceptance
circle on the calibration result window. This circle indicates that whether we managed to record accurate
data during calibration. If not there is the option to recalibrate some of the calibration points.
The same accuracy value is used to draw the acceptance circle on the validation screen. So the user /
experimenter can decide whether the calibration was successful.

### runValidation(pointDict = None, valWin = None)
Shows real time gaze position and draws several reference points (**pointDict** is a dictionary with numbered keys
and coordinate values for drawing those points) to check calibration quality. If no value for **pointDict** is given,
reference points will be drawn at the standard locations for a 5 point calibration.
valWin is a psychopy.visual.Window object. If this parameter is set the validation screen is drawn in the specified
window. Otherwise a new validation window is created.

### runTrackBox(trackWin = None)
Shows real time eye position within in the Tobii eyetracker trackbox. Uses colors and reported eye distance to let
the subject know if they are well positioned relative to the tracker.
trackWin is a psychopy.visual.Window object. If this parameter is set the track box screen is drawn in the specified
window. Otherwise a new track box window is created.

### runFullCalibration(numCalibPoints = None, calibWin = None)
Runs a full 5 or 9 point calibration routine as specified by **numCalibPoints**. If **numCalibPoints** is not defined,
then the default is a 9 point calibration. This full calibration routine includes: finding eye positions within the trackbox,
running a calibration, showing calibration accuracy, re-calibrating problem points, checking the quality of the calibration, and
saving the calibration to the eyetracker. Requires a working keyboard to control.
calibWin is a psychopy.visual.Window object. If this parameter is set the calibration screen is drawn in the specified
window. Otherwise a new calibration window is created.

## Examples

Init a TobiiHelper object, set the default monitor, set the default eye tracker
and run a full 5-point calibration:

```
# Import the calibration module
import tobii_calibration as tc

# Create a TobiiHelper object
tobii_helper = tc.TobiiHelper()

# Idenfity and define the experimental monitor
tobii_helper.setMonitor()

# Find eyetrackers and connect
tobii_helper.setEyeTracker()

# Run a full 5 point calibration routing
tobii_helper.runFullCalibration(numCalibPoints = 5)

```

## Authors

**Tamás Zolnai** - *Maintaining, module rework* - [tzolnai](https://github.com/tzolnai)

**Olivia Guayasamin** - *Initial work as tobii-pro-wrapper* - [oguayasa](https://github.com/oguayasa)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/tzolnai/tobii_calibration/blob/master/LICENSE.txt) file for details.



