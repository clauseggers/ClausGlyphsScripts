#MenuTitle: Sets side-bearings of all layers of current glyph to 30
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Sets the side-bearings of all the layers of the current glyph to 30.
"""

for layer in Glyphs.font.selectedLayers:
	# Access to the glyph
	glyph = layer.parent
	# Access to all layers of the glyph
	for layer in glyph.layers:
		layer.RSB = 30

# EOF