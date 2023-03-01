#MenuTitle: Free the vertical alignment, but preserve the horizontal
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Frees the vertical alignment, but preserves the horizontal.
"""

for layer in Glyphs.font.selectedLayers:
	# Access to the glyph
	glyph = layer.parent
	# Access to all layer of the glyph
	for layer in glyph.layers:
		# Copy layer to its background
		layer.shapes[0].alignment = 3

# EOF