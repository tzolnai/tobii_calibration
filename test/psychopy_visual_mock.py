# Authors:
# Tamás Zolnai (zolnaitamas2000@gmail.com)

# License: Apache License 2.0, see LICENSE.txt for more details.

from psychopy import visual

listOfDrawings = []

# override visual methods, to check the drawing objects without actually drawing
def RectangleDraw(rectangle):
    rect_copy = Rect()
    rect_copy.pos = rectangle.pos
    rect_copy.width = rectangle.width
    rect_copy.height = rectangle.height
    listOfDrawings.append(rect_copy)

visual.Rect.draw = RectangleDraw

def CircleDraw(circle):
    circle_copy = Circle()
    circle_copy.radius = circle.radius
    circle_copy.pos = circle.pos
    circle_copy.fillColor = circle.fillColor
    circle_copy.lineColor = circle.lineColor
    listOfDrawings.append(circle_copy)

visual.Circle.draw = CircleDraw

def LineDraw(line):
    line_copy = Line()
    line_copy.start = line.start
    line_copy.end = line.end
    line_copy.lineWidth = line.lineWidth
    line_copy.lineColor = line.lineColor
    listOfDrawings.append(line_copy)

visual.Line.draw = LineDraw

def TextStimDraw(textStim):
    test_stim_copy = TextStim()
    test_stim_copy.height = textStim.height
    test_stim_copy.pos = textStim.pos
    test_stim_copy.color = textStim.color
    test_stim_copy.text = textStim.text
    listOfDrawings.append(test_stim_copy)

visual.TextStim.draw = TextStimDraw

def WindowFlip(window):
    pass

visual.Window.flip = WindowFlip

class Rect:

    def __init__(self):
        pos = None
        width = None
        height = None

class Circle:

    def __init__(self):
        pos = None
        radius = None
        fillColor = None
        lineColor = None

class Line:

    def __init__(self):
        start = None
        end = None
        lineWidth = None
        lineColor = None

class TextStim:

    def __init__(self):
        pos = None
        height = None
        color = None
        text = None


class PsychoPyVisualMock:

    def __init__(self):

        global listOfDrawings
        listOfDrawings = []

    def getListOfDrawings(self):
        return listOfDrawings

    def clear(self):
        listOfDrawings = []