#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MenuTitle: Set Font Info from TOML
# ShortCut:
# GlyphsVersion: 3.0
# Description: Paste TOML describing Font Info fields and apply them to the current font.

try:
	from GlyphsApp import GSPropertyNameVendorIDKey
except Exception:
	GSPropertyNameVendorIDKey = "GSPropertyNameVendorIDKey"

try:
	from AppKit import NSFont
except Exception:
	NSFont = None

from typing import Dict, Any

try:
	from GlyphsApp import Glyphs
except Exception:
	Glyphs = None

try:
	# Glyphs bundles vanilla; used for UI
	import vanilla
except Exception:
	vanilla = None



TOML_TEMPLATE = """# Paste your Font Info here and click Apply.
# Only simple key = "value" lines are needed. Multiline values are supported with triple quotes.

designer = ""  # e.g. "Jane Doe"
designerURL = ""  # e.g. "https://example.com"
manufacturer = ""  # e.g. "Example Type"
manufacturerURL = ""  # e.g. "https://type.example.com"
copyright = ""  # e.g. "© 2025 Example Type. All Rights Reserved."
license = ""  # e.g. "SIL OFL 1.1"
licenseURL = ""  # e.g. "https://scripts.sil.org/OFL"
trademark = ""  # e.g. "Example is a trademark of Example Type."
	# General
vendorID = ""  # Vendor Identification (was openTypeOS2VendorID), e.g. "EXAM"
"""


def _parse_simple_toml(text: str) -> Dict[str, Any]:
	"""
	Minimal TOML parser for key = "value" lines with optional single- or triple-quoted strings.
	Supports comments (# ...) and blank lines. Multiline values using three double quotes or three single quotes.
	Returns a dict with string values.
	"""
	data: Dict[str, Any] = {}
	lines = text.splitlines()
	i = 0
	while i < len(lines):
		raw = lines[i]
		line = raw.strip()
		i += 1
		if not line or line.startswith("#"):
			continue
		# Remove inline comments that start with # not inside quotes (simple heuristic)
		def _strip_inline_comment(s: str) -> str:
			out = []
			in_single = False
			in_double = False
			j = 0
			while j < len(s):
				ch = s[j]
				if ch == "'" and not in_double:
					in_single = not in_single
					out.append(ch)
				elif ch == '"' and not in_single:
					in_double = not in_double
					out.append(ch)
				elif ch == "#" and not in_single and not in_double:
					break
				else:
					out.append(ch)
				j += 1
			return "".join(out).rstrip()

		line = _strip_inline_comment(line)
		if not line or "=" not in line:
			continue
		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip()

		# Multiline triple-quoted strings
		triple_double = '"""'
		triple_single = "'''"
		if value.startswith(triple_double):
			if value.endswith(triple_double) and len(value) > 3:
				# Single-line triple-quoted
				data[key] = value[3:-3]
				continue
			# Accumulate until closing """
			acc = [value[3:]]
			while i < len(lines):
				part = lines[i]
				i += 1
				if part.endswith(triple_double):
					acc.append(part[:-3])
					break
				acc.append(part)
			data[key] = "\n".join(acc)
			continue
		if value.startswith(triple_single):
			if value.endswith(triple_single) and len(value) > 3:
				data[key] = value[3:-3]
				continue
			acc = [value[3:]]
			while i < len(lines):
				part = lines[i]
				i += 1
				if part.endswith(triple_single):
					acc.append(part[:-3])
					break
				acc.append(part)
			data[key] = "\n".join(acc)
			continue

		# Quoted string
		if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
			data[key] = value[1:-1]
			continue

		# Bare value (treat as string)
		data[key] = value
	return data


def _parse_toml(text: str) -> Dict[str, Any]:
	# Try stdlib tomllib (Py 3.11+)
	try:
		import tomllib  # type: ignore
		return tomllib.loads(text)
	except Exception:
		pass
	# Try external 'toml' if available
	try:
		import toml  # type: ignore
		return toml.loads(text)
	except Exception:
		pass
	# Fallback to minimal parser
	return _parse_simple_toml(text)


def _set_font_info_from_dict(font, info: Dict[str, Any]) -> Dict[str, str]:
	"""Apply supported keys from info to the given GSFont. Returns a report dict of changes."""
	if not font:
		raise RuntimeError("No font open. Open a font and try again.")
	key_map = {
		"designer": "designer",
		"designerURL": "designerURL",
		"manufacturer": "manufacturer",
		"manufacturerURL": "manufacturerURL",
		"copyright": "copyright",
		"license": "license",
		"trademark": "trademark",
	}

	changes: Dict[str, str] = {}

	# Set all mapped fields (direct attributes)
	for k, attr in key_map.items():
		if k in info:
			new_val = info.get(k)
			try:
				old_val = getattr(font, attr, None)
				setattr(font, attr, new_val)
				changes[attr] = f"{old_val!r} -> {new_val!r}"
			except Exception:
				print(f"[SetMetaInfo][ERROR] Could not set {attr}")
				changes[attr] = f"FAILED to set (unknown -> {new_val!r})"

	# Helper for custom property setting (used by mekkablue's script)
	def addPropertyToFont(font, key, value):
		try:
			while font.propertyForName_(key):
				font.removeObjectFromProperties_(font.propertyForName_(key))
			font.setProperty_value_languageTag_(key, value, None)
		except Exception as e:
			print(f"[SetMetaInfo][ERROR] Could not set property {key}: {e}")

	# Set vendorID as a custom property
	if "vendorID" in info:
		new_val = info["vendorID"]
		try:
			existing = font.propertyForName_("vendorID")
			old_val = existing.value if existing else None
			addPropertyToFont(font, "vendorID", new_val)
			changes["vendorID"] = f"{old_val!r} -> {new_val!r}"
		except Exception as e:
			print(f"[SetMetaInfo][ERROR] Could not set vendorID: {e}")
			changes["vendorID"] = f"FAILED to set (unknown -> {new_val!r})"

	# Set licenseURL as a custom property
	if "licenseURL" in info:
		new_val = info["licenseURL"]
		try:
			existing = font.propertyForName_("licenseURL")
			old_val = existing.value if existing else None
			addPropertyToFont(font, "licenseURL", new_val)
			changes["licenseURL"] = f"{old_val!r} -> {new_val!r}"
		except Exception as e:
			print(f"[SetMetaInfo][ERROR] Could not set licenseURL: {e}")
			changes["licenseURL"] = f"FAILED to set (unknown -> {new_val!r})"

	return changes


class SetFontInfoFromTOMLUI(object):
	def __init__(self):
		if vanilla is None:
			raise RuntimeError("vanilla module not available. Please run inside Glyphs app.")

		width, height = 640, 520
		self.w = vanilla.FloatingWindow((width, height), "Set Font Info from TOML")
		pad = 12
		self.w.desc = vanilla.TextBox((pad, pad, -pad, 18), "Paste TOML below and click Apply:")
		# Load last content from Glyphs preferences if available
		_PREF_KEY = "com.clauseggers.SetMetaInfo.lastTOML"
		initial_text = TOML_TEMPLATE
		try:
			if Glyphs is not None:
				last = Glyphs.defaults[_PREF_KEY]
				if last and isinstance(last, str) and last.strip():
					initial_text = last
		except Exception:
			pass
		self.w.editor = vanilla.TextEditor((pad, 34, -pad, height - 100), text=initial_text)

		# Minimal: force plain text, set a fixed-pitch font, and disable smart substitutions
		try:
			nsTextView = None
			if hasattr(self.w.editor, "getNSTextView"):
				nsTextView = self.w.editor.getNSTextView()
			elif hasattr(self.w.editor, "getNSScrollView"):
				sv = self.w.editor.getNSScrollView()
				if sv is not None and hasattr(sv, "documentView"):
					nsTextView = sv.documentView()
			if nsTextView is not None:
				if hasattr(nsTextView, "setRichText_"):
					nsTextView.setRichText_(False)
				if hasattr(nsTextView, "setImportsGraphics_"):
					nsTextView.setImportsGraphics_(False)
				# Disable smart substitutions (quotes, dashes, etc.)
				for sel in (
					"setAutomaticQuoteSubstitutionEnabled_",
					"setAutomaticDashSubstitutionEnabled_",
					"setAutomaticTextReplacementEnabled_",
					"setAutomaticSpellingCorrectionEnabled_",
					"setContinuousSpellCheckingEnabled_",
					"setGrammarCheckingEnabled_",
					"setSmartInsertDeleteEnabled_",
				):
					if hasattr(nsTextView, sel):
						getattr(nsTextView, sel)(False)
				# Set a fixed-pitch font with good Unicode coverage
				if NSFont is not None:
					font = None
					for fam in ("SF Mono", "Menlo", "Monaco", "Courier"):
						f = NSFont.fontWithName_size_(fam, 13.0)
						if f is not None:
							font = f
							break
					if font is None and hasattr(NSFont, "userFixedPitchFontOfSize_"):
						font = NSFont.userFixedPitchFontOfSize_(13.0)
					if font is not None and hasattr(nsTextView, "setFont_"):
						nsTextView.setFont_(font)
		except Exception:
			pass
		self.w.applyButton = vanilla.Button((-200 - pad, -40 - pad, 100, 24), "Apply", callback=self.apply_)
		self.w.cancelButton = vanilla.Button((-90 - pad, -40 - pad, 80, 24), "Close", callback=self.close_)
		self.w.status = vanilla.TextBox((pad, -40 - pad, -220, 24), "")
		self.w.open()
		self.w.makeKey()

	def close_(self, sender=None):
		# Save current content to Glyphs preferences
		_PREF_KEY = "com.clauseggers.SetMetaInfo.lastTOML"
		try:
			text = self.w.editor.get()
			if Glyphs is not None:
				Glyphs.defaults[_PREF_KEY] = text
		except Exception:
			pass
		try:
			self.w.close()
		except Exception:
			pass

	def apply_(self, sender=None):
		# Save current content to Glyphs preferences
		_PREF_KEY = "com.clauseggers.SetMetaInfo.lastTOML"
		text = self.w.editor.get()
		try:
			if Glyphs is not None:
				Glyphs.defaults[_PREF_KEY] = text
		except Exception:
			pass
		try:
			data = _parse_toml(text)
		except Exception as e:
			self._notify("Could not parse TOML: %s" % e, error=True)
			return
		font = Glyphs.font if Glyphs else None
		if not font:
			self._notify("No font open.", error=True)
			return
		try:
			changes = _set_font_info_from_dict(font, data)
		except Exception as e:
			self._notify("Error applying values: %s" % e, error=True)
			return

		if changes:
			msg = ", ".join(sorted(changes.keys()))
			self._notify(f"Updated: {msg}")
			try:
				Glyphs.showNotification("Set Font Info", f"Applied: {msg}")
			except Exception:
				pass
		else:
			self._notify("No recognized keys.")

	def _notify(self, message: str, error: bool = False):
		try:
			self.w.status.set(message)
		except Exception:
			pass
		try:
			if error:
				print("[SetFontInfoFromTOML][ERROR]", message)
			else:
				print("[SetFontInfoFromTOML]", message)
		except Exception:
			pass


def main():
	if Glyphs is None:
		print("This script must be run from within Glyphs app.")
		return
	SetFontInfoFromTOMLUI()


if __name__ == "__main__":
	main()
