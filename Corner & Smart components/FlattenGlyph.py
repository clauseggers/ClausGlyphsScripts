# MenuTitle: Decompose all Cap & Corner components in all layers
# -*- coding: utf-8 -*-
# by Claus Eggers Sørensen
__doc__="""
Decomposes all corner components in all layers of the selected glyphs.
"""

import GlyphsApp

Font = Glyphs.font # the frontmost font
selectedLayers = Font.selectedLayers # active layers of selected glyphs

def decomposeCornersInLayer(layer):
    if hasattr(layer, 'decomposeCorners'):
        layer.decomposeCorners()

def main():
    for layer in selectedLayers:
        glyph = layer.parent
        for glyphLayer in glyph.layers:
            decomposeCornersInLayer(glyphLayer)

if __name__ == '__main__':
    main()

# EOF