#MenuTitle: Creates strings by combining placeholders and characters
#Created by Claus
# -*- coding: utf-8 -*-
__doc__="""
Creates all permutations of strings and characters
"""

from GlyphsApp import *
import vanilla

class ReplaceZerosInGlyphs:
    def __init__(self):
        self.w = vanilla.Window((300, 150), "Replace Zeros")
        self.w.inputText = vanilla.TextBox((10, 10, -10, 20), "Input string:")
        self.w.inputString = vanilla.EditText((10, 30, -10, 20), "min0a0o0s0n0h0l0j0f0uim")
        self.w.replaceText = vanilla.TextBox((10, 60, -10, 20), "Replacement chars:")
        self.w.replaceChars = vanilla.EditText((10, 80, -10, 20), "ɓƈɗɠɦƙɲƥɋɾƭʈʋⱳƴɖɋɽʈjɩʃɾɩ́ɩt")
        self.w.runButton = vanilla.Button((10, 110, -10, 20), "Run", callback=self.run)
        self.w.open()

    def replace_zeros(self, input_string, replacement_char):
        return input_string.replace('0', replacement_char)

    def run(self, sender):
        input_string = self.w.inputString.get()
        replacement_chars = self.w.replaceChars.get()

        font = Glyphs.font
        if not font:
            Message("No font open", "Please open a font and try again.")
            return

        output_strings = []
        for char in replacement_chars:
            replaced_string = self.replace_zeros(input_string, char)
            output_strings.append(replaced_string)

        # Join all strings with newline characters and create a single new tab
        full_output = "\n".join(output_strings)
        font.newTab(full_output)

ReplaceZerosInGlyphs()