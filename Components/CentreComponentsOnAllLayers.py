#MenuTitle: Centre all components on all layers
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Centres all the components in all the layers of the selected glyphs.
"""
# Disable interface update
Glyphs.font.disableUpdateInterface()

from Foundation import NSMidX

for layer in Glyphs.font.selectedLayers:
	# Access to the glyph
	glyph = layer.parent
	# Access to all layers of the glyph
	for layer in glyph.layers:
		for c in layer.shapes:
			pos = c.position
			pos.x += layer.width / 2.0 - NSMidX(c.bounds)
			c.position = pos


# Re-enable interface update
Glyphs.font.enableUpdateInterface()

# EOF
