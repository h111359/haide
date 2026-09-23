"""Validated declarative appearance; no executable CSS or remote font values."""
from __future__ import annotations
import re
from contracts import Error

THEMES = {"clear", "midnight", "warm", "contrast", "system", "custom"}
FONTS = {"system", "humanist", "serif", "arial"}
COLORS = {"bg", "surface", "raised", "text", "muted", "border", "accent", "on-accent", "positive", "warning", "danger", "focus"}


def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return values[0] * .2126 + values[1] * .7152 + values[2] * .0722


def validate_appearance(value):
    if not isinstance(value, dict) or set(value) - {"theme", "size", "custom"}:
        raise Error("appearance-schema", "Appearance accepts only theme, size, and a validated custom preset.")
    if value.get("theme") not in THEMES or type(value.get("size", 16)) is not int or not 14 <= value.get("size", 16) <= 22:
        raise Error("appearance-schema", "Select a supported theme and an integer base size from 14 to 22.")
    custom = value.get("custom")
    if value["theme"] == "custom" and custom is None:
        raise Error("appearance-schema", "A custom theme needs a named, complete declarative preset.")
    if custom is not None:
        if not isinstance(custom, dict) or set(custom) - {"name", "description", "mode", "font", "heading", "code", "colors"}:
            raise Error("appearance-schema", "Custom appearance cannot include arbitrary CSS, HTML, URLs, or style properties.")
        if not isinstance(custom.get("name"), str) or not 1 <= len(custom["name"]) <= 64 or any(ord(c) < 32 for c in custom["name"]):
            raise Error("appearance-schema", "Provide a plain custom preset name of 1–64 characters.")
        if custom.get("mode") not in ("light", "dark") or custom.get("font") not in FONTS or custom.get("heading") not in FONTS or custom.get("code", "mono") != "mono":
            raise Error("appearance-schema", "Use a supported light/dark mode and local font preset; code uses the local monospace stack.")
        colors = custom.get("colors")
        if not isinstance(colors, dict) or set(colors) != COLORS or any(not isinstance(v, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", v) for v in colors.values()):
            raise Error("appearance-schema", "Supply all semantic colors as six-digit hexadecimal values; CSS expressions are not permitted.")
        for foreground, background, minimum in (("text", "bg", 4.5), ("text", "surface", 4.5), ("muted", "surface", 4.5), ("on-accent", "accent", 4.5), ("focus", "surface", 3), ("positive", "surface", 4.5), ("warning", "surface", 4.5), ("danger", "surface", 4.5)):
            high, low = sorted((luminance(colors[foreground]), luminance(colors[background])), reverse=True)
            ratio = (high + .05) / (low + .05)
            if ratio < minimum:
                raise Error("appearance-contrast", f"{foreground} on {background} has contrast {ratio:.2f}:1; at least {minimum}:1 is required. Your draft can be corrected.", {"foreground": foreground, "background": background, "ratio": round(ratio, 2), "minimum": minimum})
    return value
