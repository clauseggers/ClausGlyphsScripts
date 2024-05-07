#MenuTitle: Interactively sets a vertical array of `to_low_N` anchors aligned with an existing anchor
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Interactively sets a vertical array of `top_low_N` anchors using an existing anchor for alignment.
"""

from GlyphsApp import *
from Foundation import NSPoint  # Import NSPoint from Foundation
from vanilla import *

font = Glyphs.font

font.disableUpdateInterface()

class AnchorDialog:
    def __init__(self):
        self.w = FloatingWindow((300, 270), "Anchor Settings")
        self.w.num_anchors_text = TextBox((10, 10, -10, 20), "Number of 'top_low_*' anchors")
        self.w.num_anchors_input = EditText((10, 35, -10, 20), placeholder="3")
        self.w.spacing_text = TextBox((10, 70, -10, 20), "Spacing between anchors")
        self.w.spacing_input = EditText((10, 95, -10, 20), placeholder="20")
        self.w.delete_existing_anchors = CheckBox((10, 130, -10, 20), "Delete existing 'top_low_*' anchors", value=False)
        self.w.anchor_choice_text = TextBox((10, 165, -10, 20), "Anchor to align to:")
        self.w.anchor_choice_input = PopUpButton((10, 190, -10, 20), ["top", "_top"], callback=self.anchor_choice_callback)
        self.w.ok_button = Button((10, 220, -10, 20), "Enter", callback=self.ok_callback)
        self.w.bind("resize", self.resize_window)
        self.w.open()

    def resize_window(self, sender):
        self.w.num_anchors_text.setPosSize((10, 10, -10, 20))
        self.w.num_anchors_input.setPosSize((10, 35, -10, 20))
        self.w.spacing_text.setPosSize((10, 70, -10, 20))
        self.w.spacing_input.setPosSize((10, 95, -10, 20))
        self.w.delete_existing_anchors.setPosSize((10, 130, -10, 20))
        self.w.anchor_choice_text.setPosSize((10, 165, -10, 20))
        self.w.anchor_choice_input.setPosSize((10, 190, -10, 20))
        self.w.ok_button.setPosSize((10, 220, -10, 20))

    def anchor_choice_callback(self, sender):
        pass

    def ok_callback(self, sender):
        num_anchors = int(self.w.num_anchors_input.get())
        spacing = int(self.w.spacing_input.get())
        delete_existing_anchors = self.w.delete_existing_anchors.get()
        anchor_choice = self.w.anchor_choice_input.getItems()[self.w.anchor_choice_input.get()]
        print("Number of anchors:", num_anchors)
        print("Spacing between anchors:", spacing)
        print("Delete existing anchors:", delete_existing_anchors)
        print("Anchor choice:", anchor_choice)
        self.w.close()
        create_anchors(num_anchors, spacing, delete_existing_anchors, anchor_choice)

def create_anchors(num_anchors, spacing, delete_existing_anchors, anchor_choice):
    # Define anchor names
    anchor_names = [anchor_choice] + ["top_low_" + str(i) for i in range(1, num_anchors+1)]

    selected_layers = font.selectedLayers

    for selected_layer in selected_layers:
        font_master = selected_layer.master
        glyph = selected_layer.parent
        for layer in glyph.layers:
            print("Processing layer:", layer.name)
            existing_low_anchors = []  # List to store existing low anchors to delete later
            for anchor in layer.anchors:
                if anchor.name.startswith("top_low_"):
                    existing_low_anchors.append(anchor)

            if delete_existing_anchors:
                print("Deleting existing low anchors:", [anchor.name for anchor in existing_low_anchors])
                # Remove existing low anchors
                for anchor in existing_low_anchors:
                    layer.removeAnchor_(anchor)

            existing_anchor = layer.anchors[anchor_choice]
            if existing_anchor:
                x_coordinate = existing_anchor.position.x
                y_coordinate = existing_anchor.position.y
                for anchor_name in anchor_names:
                    if anchor_name != anchor_choice:
                        y_coordinate -= spacing
                    layer.anchors.append(GSAnchor(anchor_name, NSPoint(x_coordinate, y_coordinate)))
            else:
                print("No '{}' anchor found in layer: {}".format(anchor_choice, layer.name))
    print("Anchors creation complete")

AnchorDialog()

font.enableUpdateInterface()

# EOF
