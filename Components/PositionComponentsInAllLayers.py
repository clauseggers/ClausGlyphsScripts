#MenuTitle: Position components vertically in all layers
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Position components of selected glyphs to the vertical coordinate you are prompted for in all layers.
"""
# First get a value from the user
from robofab.interface.all.dialogs import AskString
shiftAmount = int(AskString("Enter vertical position"))

# Disable interface update
Glyphs.font.disableUpdateInterface()

# First unlock the automatic alignment
for layer in Glyphs.font.selectedLayers:
    # Access to the glyph
    glyph = layer.parent
    # Access to all layer of the glyph
    for layer in glyph.layers:
        # Unlock the automatic alignment
        # https://docu.glyphsapp.com/Core/Constants/GSComponentAlignment.html
        layer.shapes[0].alignment = -1

# Then shift all the components
for layer in Glyphs.font.selectedLayers:
    # Access to the glyph
    glyph = layer.parent
    # Access to all layers of the glyph
    for layer in glyph.layers:
        for component in layer.components:
            component.automaticAlignment = False
            x, y = component.position
            component.position = (x, shiftAmount)

# Now re-enable the locked side-bearings
for layer in Glyphs.font.selectedLayers:
    # Access to the glyph
    glyph = layer.parent
    # Access to all layer of the glyph
    for layer in glyph.layers:
        # Enable only horizontal alignment
        layer.shapes[0].alignment = 3

# Re-enable interface update
Glyphs.font.enableUpdateInterface()

# EOF
