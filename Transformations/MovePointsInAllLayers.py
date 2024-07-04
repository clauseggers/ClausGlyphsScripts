#MenuTitle: Move selected points in all layers
#Created by Claus
# -*- coding: utf-8 -*-
__doc__ = """
Moves the selected points in all the layers
"""

import GlyphsApp
from GlyphsApp import Glyphs, Message
from vanilla import FloatingWindow, TextBox, EditText, CheckBox, Button
from math import tan, radians
from AppKit import NSPoint, NSEvent

class MoveSelectedObjects:
    def __init__(self):
        self.w = FloatingWindow((250, 160), "Move Selected Objects", minSize=(250, 160))

        self.w.text_horizontal = TextBox((10, 10, 90, 20), "Horizontal:")
        self.w.horizontal = EditText((100, 10, 130, 20), callback=self.saveValues)

        self.w.text_vertical = TextBox((10, 40, 90, 20), "Vertical:")
        self.w.vertical = EditText((100, 40, 130, 20), callback=self.saveValues)

        self.w.respect_italic_angle = CheckBox((10, 70, 220, 20), "Respect Italic Angle", callback=self.saveValues)

        self.w.runButton = Button((10, 110, -10, 20), "Move", callback=self.moveObjects)

        self.loadValues()

        self.w.open()
        self.w.bind("close", self.saveValues)
        self.w.bind("windowDidBecomeKey", self.setupEventMonitor)

    def setupEventMonitor(self, sender):
        NSEvent.addLocalMonitorForEventsMatchingMask_handler_(NSEvent.keyDownMask(), self.keyDown)

    def keyDown(self, event):
        if event.keyCode() == 36:  # Enter key keyCode is 36
            self.moveObjects(None)
            return None  # Prevents the default action
        return event

    def saveValues(self, sender=None):
        Glyphs.defaults["com.yourname.MoveSelectedObjects.horizontal"] = self.w.horizontal.get()
        Glyphs.defaults["com.yourname.MoveSelectedObjects.vertical"] = self.w.vertical.get()
        Glyphs.defaults["com.yourname.MoveSelectedObjects.respectItalicAngle"] = self.w.respect_italic_angle.get()

    def loadValues(self):
        self.w.horizontal.set(Glyphs.defaults.get("com.yourname.MoveSelectedObjects.horizontal", "0"))
        self.w.vertical.set(Glyphs.defaults.get("com.yourname.MoveSelectedObjects.vertical", "0"))
        self.w.respect_italic_angle.set(Glyphs.defaults.get("com.yourname.MoveSelectedObjects.respectItalicAngle", False))

    def moveObjects(self, sender):
        try:
            horizontal = float(self.w.horizontal.get())
            vertical = float(self.w.vertical.get())
            respectItalicAngle = self.w.respect_italic_angle.get()
        except ValueError:
            Message("Invalid input", "Please enter valid numbers for horizontal and vertical values.")
            return

        font = Glyphs.font
        if font is None:
            Message("No font open", "Please open a font before running the script.")
            return

        selectedLayers = font.selectedLayers
        selectedGlyphs = [l.parent for l in selectedLayers]

        for glyph in selectedGlyphs:
            for layer in glyph.layers:
                deltaX = horizontal
                deltaY = vertical

                if respectItalicAngle and font.masters[0].italicAngle != 0.0:
                    italicAngle = font.masters[0].italicAngle
                    angleRadians = radians(italicAngle)
                    deltaX += vertical * tan(angleRadians)

                for path in layer.paths:
                    for node in path.nodes:
                        if node.selected:
                            node.x += deltaX
                            node.y += deltaY

                for component in layer.components:
                    if component.selected:
                        component.transformBy((1, 0, 0, 1, deltaX, deltaY))

                for anchor in layer.anchors:
                    if anchor.selected:
                        anchor.position = NSPoint(anchor.position.x + deltaX, anchor.position.y + deltaY)

        self.saveValues()
        self.w.close()

MoveSelectedObjects()


#EOF