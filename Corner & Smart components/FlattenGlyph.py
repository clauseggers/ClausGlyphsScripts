# MenuTitle: Decompose all Cap & Corner components in all layers
# -*- coding: utf-8 -*-
# by Claus Eggers Sørensen
from __future__ import division, print_function, unicode_literals
__doc__="""
Decomposes all corner components in selected glyphs.
"""
from GlyphsPython import GSApplication, GSLayer

# Get the Glyphs application object
app = GSApplication()

# Get the current font
font = app.activeFont

# Check if a glyph is selected
if font.selection():
  # Get the selected layer
  layer = font.selection()[0]

  # Decompose all corners and caps in the layer
  layer.decomposeCorners()

  print("Decomposed all smart corners and caps in the active layer.")
else:
  print("Please select a glyph first.")

# EOF