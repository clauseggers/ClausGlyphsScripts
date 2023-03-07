#MenuTitle: Disable automatic alignment of all components in all layers
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Disables automatic alignment of all components in all layers.
"""

from GlyphsApp import *
f = Glyphs.font

f.disableUpdateInterface()

for layer in f.selectedLayers:
    # Access to the glyph
    glyph = layer.parent
    # Access to all layer of the glyph
    for layer in glyph.layers:
        # Set automatic alignment
        # https://docu.glyphsapp.com/Core/Constants/GSComponentAlignment.html
        layer.shapes[0].alignment = -1
        for component in layer.components:
            component.automaticAlignment = False


# for glyph in f.glyphs:
#     if glyph.selected:
#         for layer in glyph.layers:
#             for component in layer.components:
#                 component.automaticAlignment = True

f.enableUpdateInterface()

# EOF
