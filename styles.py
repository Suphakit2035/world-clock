"""
Style and theme configuration for World Clock.
"""

from tkinter import ttk

# Color Palette
BG_COLOR = "#F8FAFC"         # Slate 50
CARD_BG = "#FFFFFF"          # White
TEXT_PRIMARY = "#0F172A"     # Slate 900
TEXT_SECONDARY = "#64748B"   # Slate 500
ACCENT_BLUE = "#2563EB"      # Blue 600
BORDER_COLOR = "#E2E8F0"     # Slate 200

# Badges and Indicators
BADGE_BG_LOCAL = "#F1F5F9"   # Slate 100
BADGE_FG_LOCAL = "#475569"   # Slate 600
BADGE_BG_TARGET = "#DBEAFE"  # Blue 100
BADGE_FG_TARGET = "#2563EB"  # Blue 600
ERROR_COLOR = "#DC2626"      # Red 600

# Typography
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_CARD_TITLE = ("Segoe UI", 9, "bold")
FONT_TIME = ("Segoe UI", 26, "bold")
FONT_DATE = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 9, "bold")
FONT_BADGE = ("Segoe UI", 9, "bold")
FONT_DIFF = ("Segoe UI", 9)
FONT_COMBOBOX = ("Segoe UI", 10)


def configure_theme(root, style: ttk.Style) -> None:
    """Apply ttk and root window theme settings."""
    root.configure(bg=BG_COLOR)

    if "clam" in style.theme_names():
        style.theme_use("clam")

    style.configure(
        "TCombobox",
        fieldbackground=CARD_BG,
        background=BADGE_BG_LOCAL,
        foreground=TEXT_PRIMARY,
        arrowcolor=TEXT_PRIMARY,
        padding=6,
    )

