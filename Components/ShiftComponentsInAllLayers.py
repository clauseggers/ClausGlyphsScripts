#MenuTitle: Shift components in all layers
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Vertically shifts components of selected glyphs by an amount you are prompted for.
"""
# First get a value from the user
from robofab.interface.all.dialogs import AskString
shiftAmount = int(AskString("Enter vertical shift"))

# Then shift all the components
for layer in Glyphs.font.selectedLayers:
	# Access to the glyph
	glyph = layer.parent
	# Access to all layers of the glyph
	for layer in glyph.layers:
		for component in layer.components:
			component.automaticAlignment = False
			x, y = component.position
			component.position = (x, y + shiftAmount)

# Now re-enables the locked side-bearings
for layer in Glyphs.font.selectedLayers:
	# Access to the glyph
	glyph = layer.parent
	# Access to all layer of the glyph
	for layer in glyph.layers:
		# Copy layer to its background
		layer.shapes[0].alignment = 3

# EOF