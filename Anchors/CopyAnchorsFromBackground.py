# MenuTitle: Copy anchors from background to front layers
# Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Copies anchors from the background layers to the front layers in the selected glyphs.
"""

from GlyphsApp import *

def copy_anchors_from_background():
    """
    Copies anchors from background layers to front layers in selected glyphs.
    """
    font = Glyphs.font
    if not font:
        print("Error: No font open")
        return

    selected_glyphs = [layer.parent for layer in font.selectedLayers]
    if not selected_glyphs:
        print("Error: No glyphs selected")
        return

    copied_count = 0
    processed_glyphs = 0

    for glyph in selected_glyphs:
        processed_glyphs += 1

        for layer in glyph.layers:
            # Only process regular (foreground) layers
            if layer.isSpecialLayer:
                continue

            # Access the background layer for this layer
            background_layer = layer.background

            if background_layer is None:
                continue

            if not hasattr(background_layer, 'anchors') or not background_layer.anchors:
                continue

            # Copy anchors from background to front layer
            anchors_copied_in_layer = 0
            for anchor in background_layer.anchors:
                # Check if anchor already exists in front layer
                existing_anchor = None
                for existing in layer.anchors:
                    if existing.name == anchor.name:
                        existing_anchor = existing
                        break

                if existing_anchor:
                    # Update position of existing anchor
                    existing_anchor.position = anchor.position
                else:
                    # Create new anchor
                    new_anchor = GSAnchor()
                    new_anchor.name = anchor.name
                    new_anchor.position = anchor.position
                    layer.anchors.append(new_anchor)

                anchors_copied_in_layer += 1

            if anchors_copied_in_layer > 0:
                copied_count += anchors_copied_in_layer

    # Only show message if no anchors were found (failure case)
    if copied_count == 0:
        print("No anchors found in background layers of selected glyphs")

# Execute the function
copy_anchors_from_background()
