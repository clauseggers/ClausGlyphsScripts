#MenuTitle: Interactively set a vertical array of `top` anchors
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Interactively set a vertical array of `top_low_N` anchors using the existing `top` or `_top` anchor for alignment.
"""

from GlyphsApp import *
from Foundation import NSPoint, NSAffineTransform, NSAffineTransformStruct  # Import NSPoint and NSAffineTransform from Foundation
from math import tan, radians  # Import tan and radians from math
from vanilla import *

font = Glyphs.font

font.disableUpdateInterface()

class AnchorDialog:
    def __init__(self):
        self.w = FloatingWindow((300, 230), "Anchor Settings")
        self.w.num_anchors_text = TextBox((10, 10, -10, 20), "Number of 'top_low_*' anchors")
        self.w.num_anchors_input = EditText((10, 35, -10, 20), placeholder="3")
        self.w.spacing_text = TextBox((10, 70, -10, 20), "Spacing between anchors")
        self.w.spacing_input = EditText((10, 95, -10, 20), placeholder="20")
        self.w.delete_existing_anchors = CheckBox((10, 130, -10, 20), "Delete existing 'top_low_*' anchors", value=False)
        self.w.ok_button = Button((10, 160, -10, 20), "Enter", callback=self.ok_callback)
        self.w.bind("resize", self.resize_window)
        self.w.open()

    def resize_window(self, sender):
        self.w.num_anchors_text.setPosSize((10, 10, -10, 20))
        self.w.num_anchors_input.setPosSize((10, 35, -10, 20))
        self.w.spacing_text.setPosSize((10, 70, -10, 20))
        self.w.spacing_input.setPosSize((10, 95, -10, 20))
        self.w.delete_existing_anchors.setPosSize((10, 130, -10, 20))
        self.w.ok_button.setPosSize((10, 160, -10, 20))

    def ok_callback(self, sender):
        num_anchors = int(self.w.num_anchors_input.get())
        spacing = int(self.w.spacing_input.get())
        delete_existing_anchors = self.w.delete_existing_anchors.get()
        print("Number of anchors:", num_anchors)
        print("Spacing between anchors:", spacing)
        print("Delete existing anchors:", delete_existing_anchors)
        self.w.close()
        create_anchors(num_anchors, spacing, delete_existing_anchors)

def create_anchors(num_anchors, spacing, delete_existing_anchors):
    # Define anchor names
    anchor_names = ["top"] + ["top_low_" + str(i) for i in range(1, num_anchors+1)]

    selected_layers = font.selectedLayers

    for selected_layer in selected_layers:
        glyph = selected_layer.parent
        for layer in glyph.layers:
            print("Processing layer:", layer.name)
            existing_low_anchors = []  # List to store existing low anchors to delete later
            for anchor in layer.anchors:
                if anchor.name.startswith("top_low_"):
                    existing_low_anchors.append(anchor)

            if delete_existing_anchors:
                print("Deleting existing low anchors:", [anchor.name for anchor in existing_low_anchors])
                # Remove existing low anchors
                for anchor in existing_low_anchors:
                    layer.removeAnchor_(anchor)

            reference_anchor = layer.anchors["top"]
            if reference_anchor:
                reference_position = NSPoint(reference_anchor.position.x, reference_anchor.position.y)
                italic_angle = layer.master.italicAngle
                for index, anchor_name in enumerate(anchor_names[1:], start=1):
                    # Calculate new anchor position
                    x_offset = spacing * index * tan(radians(italic_angle))
                    new_y = reference_position.y - spacing * index
                    new_x = reference_position.x - x_offset
                    print(f"Anchor name: {anchor_name}")
                    print(f"Final position: {NSPoint(new_x, new_y)}")
                    layer.anchors.append(GSAnchor(anchor_name, NSPoint(new_x, new_y)))
            else:
                print("No 'top' anchor found in layer:", layer.name)
    print("Anchors creation complete")

AnchorDialog()

font.enableUpdateInterface()

# EOF
