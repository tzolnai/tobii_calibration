# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

from psychopy import visual

listOfDrawings = []

# override visual methods, to check the drawing objects without actually drawing
def RectangleDraw(rectangle):
    listOfDrawings.append(rectangle)

visual.Rect.draw = RectangleDraw

def CircleDraw(circle):
    listOfDrawings.append(circle)

visual.Circle.draw = CircleDraw

def TextStimDraw(textStim):
    listOfDrawings.append(textStim)

visual.TextStim.draw = TextStimDraw

def WindowFlip(window):
    pass

visual.Window.flip = WindowFlip

class PsychoPyVisualMock:

    def __init__(self):

        global listOfDrawings
        listOfDrawings = []

    def getListOfDrawings(self):
        return listOfDrawings

    def clearListOfDrawings(self):
        listOfDrawings = []