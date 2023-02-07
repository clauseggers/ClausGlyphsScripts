#MenuTitle: Copies all layers of the selected glyphs to their backgrounds
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Copies all layers of the selected glyphs to their backgrounds.
"""

for layer in Glyphs.font.selectedLayers:
	# Access to the glyph 
	glyph = layer.parent
	# Access to all layer of the glyph
	for layer in glyph.layers:
		# Copy layer to its background
		layer.background = layer.copy()

# EOF