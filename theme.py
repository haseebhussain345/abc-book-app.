"""Colour themes for ABC Kids.

Designed for eye comfort and colour-vision deficiency:
* warm off-white / soft dark backgrounds (no pure white or pure black glare)
* every text/background pair is checked to meet WCAG contrast (see tests)
* colour never carries meaning alone: buttons also differ by label, icon and
  position, and the Primary/Listen pair is the blue/orange pair that stays
  distinguishable for protanopia, deuteranopia and tritanopia.
"""


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def hex_to_rgba(value, alpha=1.0):
    r, g, b = hex_to_rgb(value)
    return (r / 255.0, g / 255.0, b / 255.0, alpha)


def _channel(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(value):
    r, g, b = (_channel(c) for c in hex_to_rgb(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


THEMES = {
    "day": {
        "bg": "#FFF8E8",
        "text": "#1F2A44",
        "subtext": "#3D4A66",
        "accent": "#005A8C",
        "tints": ["#D6ECFA", "#FFF0B8", "#DDF2E4", "#FBE1EC", "#E6DFF7", "#FFE3CC"],
        "sticker": "#FFFDF6",
        "chip_bg": "#EADFC4", "chip_text": "#1F2A44",
        "primary_bg": "#0072B2", "primary_text": "#FFFFFF",
        "listen_bg": "#E69F00", "listen_text": "#1F2A44",
        "soft_bg": "#DDE3EF", "soft_text": "#1F2A44",
        "track": "#DCD2B8", "fill": "#0072B2",
        "panel": "#FFF8E8",
    },
    "night": {
        "bg": "#1D2233",
        "text": "#F6EBD3",
        "subtext": "#D5CCB8",
        "accent": "#FFD166",
        "tints": ["#2D4068", "#4A4126", "#29483E", "#4B3350", "#3B3A5E", "#503A2C"],
        "sticker": "#EFE6D2",
        "chip_bg": "#2E3652", "chip_text": "#F6EBD3",
        "primary_bg": "#56B4E9", "primary_text": "#14213D",
        "listen_bg": "#E69F00", "listen_text": "#14213D",
        "soft_bg": "#39425F", "soft_text": "#F6EBD3",
        "track": "#3A4263", "fill": "#56B4E9",
        "panel": "#252B42",
    },
}


def get_theme(name):
    return THEMES.get(name, THEMES["day"])
