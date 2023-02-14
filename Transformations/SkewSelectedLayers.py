#MenuTitle: Skew selected layers, but not components
#Created by Georg
# -*- coding: utf-8 -*-
__doc__="""
Skews the selected layers of the selected glyph(s), but does not slant the components.
"""

import GlyphsApp
import math
from AppKit import NSAffineTransform

def slantLayers(layers, angle):
	Font.disableUpdateInterface()
	slantHeight = layers[0].slantHeight()
	transform = NSAffineTransform.new()
	slant = math.tan(skewAngle * math.pi / 180.0)
	transform.shearXBy_atCenter_(slant, -slantHeight)

	for layer in layers:
		layer.transform_checkForSelection_(transform, False)

	Font.enableUpdateInterface()

palettes = Font.parent.windowController().panelSidebarViewController().valueForKey_("paletteInstances")
for palette in palettes:
	if "GlyphsPaletteLayers" in palette.__class__.__name__:
		break
selectedRows = palette.layersList().selectedRowIndexes()
layers = palette.allSelectedLayers_(selectedRows)

from robofab.interface.all.dialogs import AskString
skewAngle = float(AskString("Enter skew angle"))
slantLayers(layers, skewAngle)

# EOF