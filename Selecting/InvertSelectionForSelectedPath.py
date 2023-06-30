#MenuTitle: Invert Selection of Selected Path
#Created by Florian
# -*- coding: utf-8 -*-
__doc__="""
Inverts the selection of a selected path.
"""

selected_paths = set([x.parent for x in Layer.selection if type(x) == GSNode])
for path in selected_paths:
    for node in path.nodes:
        node.selected = not node.selected

# EOF