#MenuTitle: Set the upper case anchors for Playfair
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Sets the upper case anchors for Playfair.
"""

from GlyphsApp import *
from Foundation import NSPoint  # Import NSPoint from Foundation

font = Glyphs.font

font.disableUpdateInterface()

# Define anchor names
anchor_names = ["test_1", "test_2", "test_3"]

# Define a dictionary to store anchor coordinates per anchor name
anchor_coordinates = {
    "test_1": [
        (10, 10),
        (10, 20),
        (10, 30),
        (10, 40),
        (10, 50),
        (10, 60),
        (10, 70),
        (10, 80)
    ],
    "test_2": [
        (20, 10),
        (20, 20),
        (20, 30),
        (20, 40),
        (20, 50),
        (20, 60),
        (20, 70),
        (20, 80)
    ],
    "test_3": [
        (30, 10),
        (30, 20),
        (30, 30),
        (30, 40),
        (30, 50),
        (30, 60),
        (30, 70),
        (30, 80)
    ]
}

selected_glyphs = font.selectedLayers

for selected_layer in selected_glyphs:
    glyph = selected_layer.parent
    for anchor_name in anchor_names:
        for layer_id, coordinate in enumerate(anchor_coordinates[anchor_name], start=1):
            if layer_id <= len(glyph.layers):
                layer = glyph.layers[layer_id - 1]
                layer.anchors.append(GSAnchor(anchor_name, NSPoint(coordinate[0], coordinate[1])))

font.enableUpdateInterface()

# EOF
