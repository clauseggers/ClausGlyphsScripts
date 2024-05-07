#MenuTitle: Interactively set top anchors in diacritics
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Interactively set a vertical array of `top_low_N` anchors using the existing `_top` anchor for alignment.
"""

from GlyphsApp import *
from Foundation import NSPoint  # Import NSPoint from Foundation
from vanilla import *

font = Glyphs.font

font.disableUpdateInterface()

class AnchorDialog:
    def __init__(self):
        self.w = FloatingWindow((300, 280), "Anchor Settings")
        self.w.top_distance_text = TextBox((10, 10, -10, 20), "Distance above x-height for 'top' anchor")
        self.w.top_distance_input = EditText((10, 35, -10, 20), placeholder="10")
        self.w.num_anchors_text = TextBox((10, 70, -10, 20), "Number of 'top_low_*' anchors")
        self.w.num_anchors_input = EditText((10, 95, -10, 20), placeholder="3")
        self.w.spacing_text = TextBox((10, 130, -10, 20), "Spacing between anchors")
        self.w.spacing_input = EditText((10, 155, -10, 20), placeholder="20")
        self.w.delete_existing_anchors = CheckBox((10, 190, -10, 20), "Delete existing 'top_low_*' anchors", value=False)
        self.w.ok_button = Button((10, 220, -10, 20), "Enter", callback=self.ok_callback)
        self.w.bind("resize", self.resize_window)
        self.w.open()

    def resize_window(self, sender):
        self.w.top_distance_input.setPosSize((10, 35, -10, 20))
        self.w.num_anchors_text.setPosSize((10, 70, -10, 20))
        self.w.num_anchors_input.setPosSize((10, 95, -10, 20))
        self.w.spacing_text.setPosSize((10, 130, -10, 20))
        self.w.spacing_input.setPosSize((10, 155, -10, 20))
        self.w.delete_existing_anchors.setPosSize((10, 190, -10, 20))
        self.w.ok_button.setPosSize((10, 220, -10, 20))

    def ok_callback(self, sender):
        top_distance = int(self.w.top_distance_input.get())
        num_anchors = int(self.w.num_anchors_input.get())
        spacing = int(self.w.spacing_input.get())
        delete_existing_anchors = self.w.delete_existing_anchors.get()
        print("Top distance:", top_distance)
        print("Number of anchors:", num_anchors)
        print("Spacing between anchors:", spacing)
        print("Delete existing anchors:", delete_existing_anchors)
        self.w.close()
        create_anchors(top_distance, num_anchors, spacing, delete_existing_anchors)

def create_anchors(top_distance, num_anchors, spacing, delete_existing_anchors):
    # Define anchor names
    anchor_names = ["top"] + ["top_low_" + str(i) for i in range(1, num_anchors+1)]

    selected_layers = font.selectedLayers

    for selected_layer in selected_layers:
        font_master = selected_layer.master
        x_height = font_master.xHeight
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

            existing_anchor = layer.anchors["_top"]
            x_coordinate = existing_anchor.position.x
            y_coordinate = existing_anchor.position.y + top_distance
            for anchor_name in anchor_names:
                if anchor_name != "top":
                    y_coordinate -= spacing
                layer.anchors.append(GSAnchor(anchor_name, NSPoint(x_coordinate, y_coordinate)))
    print("Anchors creation complete!")

AnchorDialog()

font.enableUpdateInterface()

# EOF