#MenuTitle: Set the lower-case diacritic anchors for Playfair
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Sets the lower-case diacritic anchors for Playfair.
"""

from GlyphsApp import *
from Foundation import NSPoint  # Import NSPoint from Foundation
from vanilla import *

font = Glyphs.font

font.disableUpdateInterface()

class AnchorDialog:
    def __init__(self):
        self.w = FloatingWindow((300, 250), "Anchor Settings")
        self.w.top_distance_text = TextBox((10, 10, -10, 20), "Distance above x-height for 'top' anchor:")
        self.w.top_distance_input = EditText((10, 35, -10, 20), placeholder="10")
        self.w.num_anchors_text = TextBox((10, 70, -10, 20), "Number of anchors:")
        self.w.num_anchors_input = EditText((10, 95, -10, 20), placeholder="3")
        self.w.spacing_text = TextBox((10, 130, -10, 20), "Spacing between anchors:")
        self.w.spacing_input = EditText((10, 155, -10, 20), placeholder="20")
        self.w.ok_button = Button((10, 190, -10, 20), "Enter", callback=self.ok_callback)
        self.w.bind("resize", self.resize_window)
        self.w.open()

    def resize_window(self, sender):
        self.w.top_distance_input.setPosSize((10, 35, -10, 20))
        self.w.num_anchors_text.setPosSize((10, 70, -10, 20))
        self.w.num_anchors_input.setPosSize((10, 95, -10, 20))
        self.w.spacing_text.setPosSize((10, 130, -10, 20))
        self.w.spacing_input.setPosSize((10, 155, -10, 20))
        self.w.ok_button.setPosSize((10, 190, -10, 20))

    def ok_callback(self, sender):
        top_distance = int(self.w.top_distance_input.get())
        num_anchors = int(self.w.num_anchors_input.get())
        spacing = int(self.w.spacing_input.get())
        self.w.close()
        create_anchors(top_distance, num_anchors, spacing)

def create_anchors(top_distance, num_anchors, spacing):
    # Define anchor names
    anchor_names = ["top"] + ["top_low_" + str(i) for i in range(1, num_anchors)]

    selected_layers = font.selectedLayers

    for selected_layer in selected_layers:
        font_master = selected_layer.master
        x_height = font_master.xHeight
        glyph = selected_layer.parent
        for layer in glyph.layers:
            existing_anchor = layer.anchors["_top"]
            x_coordinate = existing_anchor.position.x
            y_coordinate = existing_anchor.position.y + top_distance
            for anchor_name in anchor_names:
                if anchor_name != "top":
                    y_coordinate -= spacing
                existing_anchor = layer.anchors[anchor_name]
                if existing_anchor:
                    layer.removeAnchor_(existing_anchor)
                layer.anchors.append(GSAnchor(anchor_name, NSPoint(x_coordinate, y_coordinate)))

AnchorDialog()

font.enableUpdateInterface()

# EOF
