#MenuTitle: Clear test-install
#Created by Georg
# -*- coding: utf-8 -*-
__doc__="""
Clear from working memory the fonts generated into it by using the ‘Test’ install functionality.
"""

from CoreText import CTFontManagerCopyAvailableFontURLs, CTFontManagerUnregisterFontsForURL, kCTFontManagerScopeSession
tempPath = GSGlyphsInfo.applicationSupportPath()
for url in CTFontManagerCopyAvailableFontURLs():
	if url.path().hasPrefix_(tempPath):
		print(url)
		CTFontManagerUnregisterFontsForURL(url, kCTFontManagerScopeSession, None)