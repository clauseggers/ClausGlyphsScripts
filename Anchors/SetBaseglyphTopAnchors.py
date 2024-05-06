#MenuTitle: Set the upper-case base-character anchors for Playfair
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Sets the upper-case base-character anchors for Playfair.
"""

from GlyphsApp import *
from Foundation import NSPoint  # Import NSPoint from Foundation

font = Glyphs.font

font.disableUpdateInterface()

# Define anchor names
anchor_names = ["top", "top_low_10", "top_low_20"]

# Define a dictionary to store anchor coordinates per anchor name
anchor_coordinates = {
    "top": [
        (0, 708), # Needlepoint SemiCondensed
        (0, 708), # Needlepoint SemiExpanded
        (0, 708), # Needlepoint Black SemiCondensed
        (0, 708), # Needlepoint Black SemiExpanded
        (0, 708), # Agate SemiCondensed
        (0, 708), # Agate SemiExpanded
        (0, 708), # Agate Black SemiCondensed
        (0, 708)  # Agate Black SemiExpanded
    ],
    "top_low_10": [
        (0, 698),
        (0, 698),
        (0, 698),
        (0, 698),
        (0, 698),
        (0, 698),
        (0, 698),
        (0, 698)
    ],
    "top_low_20": [
        (0, 688),
        (0, 688),
        (0, 688),
        (0, 688),
        (0, 688),
        (0, 688),
        (0, 688),
        (0, 688)
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
