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
anchor_names = ["top", "top_low_1", "top_low_2", "top_low_3", "top_low_4"]

selected_layers = font.selectedLayers

# Define a dictionary to store anchor coordinates per anchor name
anchor_coordinates = {
    "top": [
        0, 741,  # Needlepoint SemiCondensed
        0, 741,  # Needlepoint SemiExpanded
        0, 744,  # Needlepoint Black SemiCondensed
        0, 744,  # Needlepoint Black SemiExpanded
        0, 741,  # Agate SemiCondensed
        0, 741,  # Agate SemiExpanded
        0, 744,  # Agate Black SemiCondensed
        0, 744   # Agate Black SemiExpanded
    ],
    "top_low_1": [
        0, 721,
        0, 721,
        0, 724,
        0, 724,
        0, 721,
        0, 721,
        0, 724,
        0, 724
    ],
    "top_low_2": [
        0, 701,
        0, 701,
        0, 704,
        0, 704,
        0, 701,
        0, 701,
        0, 704,
        0, 704
    ],
    "top_low_3": [
        0, 681,
        0, 681,
        0, 684,
        0, 684,
        0, 681,
        0, 681,
        0, 684,
        0, 684
    ],
    "top_low_4": [
        0, 661,
        0, 661,
        0, 664,
        0, 664,
        0, 661,
        0, 661,
        0, 664,
        0, 664
    ]
}

for selected_layer in selected_layers:
    glyph = selected_layer.parent
    for index, layer in enumerate(glyph.layers):
        existing_anchor = layer.anchors["_top"]
        x_coordinate = existing_anchor.position.x
        for anchor_name in anchor_names:
            coordinate = (x_coordinate, anchor_coordinates[anchor_name][index * 2 + 1])
            existing_anchor = layer.anchors[anchor_name]
            if existing_anchor:
                layer.removeAnchor_(existing_anchor)
            layer.anchors.append(GSAnchor(anchor_name, NSPoint(coordinate[0], coordinate[1])))

font.enableUpdateInterface()

# EOF
