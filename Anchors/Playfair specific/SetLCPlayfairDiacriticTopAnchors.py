#MenuTitle: Set the lower-case diacritic anchors for Playfair
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Sets the lower-case diacritic anchors for Playfair.
"""

from GlyphsApp import *
from Foundation import NSPoint  # Import NSPoint from Foundation

font = Glyphs.font

font.disableUpdateInterface()

# Define anchor names
anchor_names = ["top", "top_low_1", "top_low_2"]

# Define a dictionary to store anchor coordinates per anchor name
anchor_coordinates = {
    "top": [
        (0, 741), # Needlepoint SemiCondensed
        (0, 741), # Needlepoint SemiExpanded
        (0, 744), # Needlepoint Black SemiCondensed
        (0, 744), # Needlepoint Black SemiExpanded
        (0, 741), # Agate SemiCondensed
        (0, 741), # Agate SemiExpanded
        (0, 744), # Agate Black SemiCondensed
        (0, 744)  # Agate Black SemiExpanded
    ],
    "top_low_1": [
        (0, 711),
        (0, 711),
        (0, 714),
        (0, 714),
        (0, 711),
        (0, 711),
        (0, 714),
        (0, 714)
    ],
    "top_low_2": [
        (0, 681),
        (0, 681),
        (0, 684),
        (0, 684),
        (0, 681),
        (0, 681),
        (0, 684),
        (0, 684)
    ]
}

selected_layers = font.selectedLayers

for selected_layer in selected_layers:
    glyph = selected_layer.parent
    for index, layer in enumerate(glyph.layers):
        for anchor_name in anchor_names:
            coordinate = anchor_coordinates[anchor_name][index]
            existing_anchor = layer.anchors[anchor_name]
            if existing_anchor:
                layer.removeAnchor_(existing_anchor)
            layer.anchors.append(GSAnchor(anchor_name, NSPoint(coordinate[0], coordinate[1])))

font.enableUpdateInterface()

# EOF
