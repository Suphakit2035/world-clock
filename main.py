"""
World Clock Desktop Application
Main entry point.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import styles
from timezones import DEFAULT_TIMEZONES


class WorldClockApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("World Clock")
        self.root.iconbitmap("logo.ico")
        self.root.geometry("480x510")
        self.root.minsize(440, 470)

        # State
        self.selected_tz_var = tk.StringVar(value="Europe/Zurich")

        # Style configuration
        self.style = ttk.Style()
        styles.configure_theme(self.root, self.style)

        # Build UI
        self.build_ui()

        # Start update loop
        self.update_clocks()

    def build_ui(self):
        container = tk.Frame(self.root, bg=styles.BG_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

        # Header title
        title_label = tk.Label(
            container,
            text="World Clock",
            font=styles.FONT_TITLE,
            bg=styles.BG_COLOR,
            fg=styles.TEXT_PRIMARY,
        )
        title_label.pack(anchor="w", pady=(0, 16))

        # --- Local Clock Card ---
        local_card_frame, local_card = self.create_card(container, "Local Time")
        local_card_frame.pack(fill=tk.X, pady=(0, 16))

        self.local_time_label = tk.Label(
            local_card,
            text="00:00:00",
            font=styles.FONT_TIME,
            bg=styles.CARD_BG,
            fg=styles.TEXT_PRIMARY,
        )
        self.local_time_label.pack(anchor="w", padx=16, pady=(0, 2))

        self.local_date_label = tk.Label(
            local_card,
            text="Loading...",
            font=styles.FONT_DATE,
            bg=styles.CARD_BG,
            fg=styles.TEXT_SECONDARY,
        )
        self.local_date_label.pack(anchor="w", padx=16, pady=(0, 6))

        self.local_offset_label = tk.Label(
            local_card,
            text="UTC Offset: --",
            font=styles.FONT_BADGE,
            bg=styles.BADGE_BG_LOCAL,
            fg=styles.BADGE_FG_LOCAL,
            padx=8,
            pady=3,
        )
        self.local_offset_label.pack(anchor="w", padx=16, pady=(0, 14))

        # --- Selected Timezone Card ---
        target_card_frame, target_card = self.create_card(container, "Selected Timezone")
        target_card_frame.pack(fill=tk.X)

        # Dropdown selection frame
        selector_frame = tk.Frame(target_card, bg=styles.CARD_BG)
        selector_frame.pack(fill=tk.X, padx=16, pady=(0, 12))

        tz_label = tk.Label(
            selector_frame,
            text="Choose Timezone:",
            font=styles.FONT_LABEL,
            bg=styles.CARD_BG,
            fg=styles.TEXT_SECONDARY,
        )
        tz_label.pack(anchor="w", pady=(0, 4))

        self.tz_combobox = ttk.Combobox(
            selector_frame,
            textvariable=self.selected_tz_var,
            values=DEFAULT_TIMEZONES,
            state="readonly",
            font=styles.FONT_COMBOBOX,
        )
        self.tz_combobox.pack(fill=tk.X)
        self.tz_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_clocks())

        # Target Time
        self.target_time_label = tk.Label(
            target_card,
            text="00:00:00",
            font=styles.FONT_TIME,
            bg=styles.CARD_BG,
            fg=styles.ACCENT_BLUE,
        )
        self.target_time_label.pack(anchor="w", padx=16, pady=(0, 2))

        # Target Date
        self.target_date_label = tk.Label(
            target_card,
            text="Loading...",
            font=styles.FONT_DATE,
            bg=styles.CARD_BG,
            fg=styles.TEXT_SECONDARY,
        )
        self.target_date_label.pack(anchor="w", padx=16, pady=(0, 6))

        # Target Offset and Relative Difference Row
        info_frame = tk.Frame(target_card, bg=styles.CARD_BG)
        info_frame.pack(anchor="w", padx=16, pady=(0, 14))

        self.target_offset_label = tk.Label(
            info_frame,
            text="UTC Offset: --",
            font=styles.FONT_BADGE,
            bg=styles.BADGE_BG_TARGET,
            fg=styles.BADGE_FG_TARGET,
            padx=8,
            pady=3,
        )
        self.target_offset_label.pack(side=tk.LEFT, padx=(0, 8))

        self.target_diff_label = tk.Label(
            info_frame,
            text="",
            font=styles.FONT_DIFF,
            bg=styles.CARD_BG,
            fg=styles.TEXT_SECONDARY,
        )
        self.target_diff_label.pack(side=tk.LEFT)

    def create_card(self, parent, title: str):
        """Create a styled card container with a subtle border and header."""
        outer = tk.Frame(parent, bg=styles.BORDER_COLOR, bd=1, relief="solid")
        card = tk.Frame(outer, bg=styles.CARD_BG)
        card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        card_title = tk.Label(
            card,
            text=title.upper(),
            font=styles.FONT_CARD_TITLE,
            bg=styles.CARD_BG,
            fg=styles.TEXT_SECONDARY,
        )
        card_title.pack(anchor="w", padx=16, pady=(12, 6))
        return outer, card

    @staticmethod
    def format_offset(dt: datetime) -> str:
        """Return formatted offset string (e.g. UTC+09:00 or UTC-04:00 with timezone code)."""
        offset = dt.utcoffset()
        if offset is None:
            return "UTC+00:00"

        total_seconds = int(offset.total_seconds())
        sign = "+" if total_seconds >= 0 else "-"
        total_seconds = abs(total_seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60

        tz_abbr = dt.strftime("%Z")
        abbr_part = f" ({tz_abbr})" if tz_abbr and not tz_abbr.startswith(("UTC", "GMT", "+", "-")) else ""
        return f"UTC{sign}{hours:02d}:{minutes:02d}{abbr_part}"

    @staticmethod
    def calculate_relative_diff(local_dt: datetime, target_dt: datetime) -> str:
        """Calculate human-readable offset relative to local time."""
        loc_off = local_dt.utcoffset()
        tgt_off = target_dt.utcoffset()
        if loc_off is None or tgt_off is None:
            return ""

        diff_seconds = int((tgt_off - loc_off).total_seconds())
        if diff_seconds == 0:
            return "(Same time as local)"

        diff_hours = diff_seconds / 3600.0
        if diff_hours.is_integer():
            hours_str = f"{abs(int(diff_hours))} hr{'s' if abs(int(diff_hours)) != 1 else ''}"
        else:
            hours_str = f"{abs(diff_hours):.1f} hrs"

        if diff_seconds > 0:
            return f"({hours_str} ahead of local)"
        else:
            return f"({hours_str} behind local)"

    def update_clocks(self):
        """Update both local and target clocks and schedule the next tick."""
        time_fmt = "%H:%M:%S"
        date_fmt = "%A, %B %d, %Y"

        # 1. Update Local Time
        local_now = datetime.now().astimezone()
        self.local_time_label.config(text=local_now.strftime(time_fmt))
        self.local_date_label.config(text=local_now.strftime(date_fmt))
        local_offset_str = self.format_offset(local_now)
        local_tzname = local_now.tzname() or "Local"
        self.local_offset_label.config(text=f"Offset: {local_offset_str} • {local_tzname}")

        # 2. Update Target Timezone Time
        tz_name = self.selected_tz_var.get()
        try:
            target_tz = ZoneInfo(tz_name)
            target_now = datetime.now(target_tz)

            self.target_time_label.config(
                text=target_now.strftime(time_fmt),
                fg=styles.ACCENT_BLUE,
            )
            self.target_date_label.config(text=target_now.strftime(date_fmt))

            target_offset_str = self.format_offset(target_now)
            self.target_offset_label.config(text=f"Offset: {target_offset_str}")

            diff_str = self.calculate_relative_diff(local_now, target_now)
            self.target_diff_label.config(text=diff_str)

        except ZoneInfoNotFoundError:
            self.target_time_label.config(text="Unknown Zone", fg=styles.ERROR_COLOR)
            self.target_date_label.config(text="Please choose a valid IANA timezone.")
            self.target_offset_label.config(text="Offset: N/A")
            self.target_diff_label.config(text="")
        except Exception as e:
            self.target_time_label.config(text="Error", fg=styles.ERROR_COLOR)
            self.target_date_label.config(text=str(e))
            self.target_offset_label.config(text="Offset: N/A")
            self.target_diff_label.config(text="")

        # Schedule next update in 1000 milliseconds (1 second)
        self.root.after(1000, self.update_clocks)


def main():
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

