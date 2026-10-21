# World Clock Desktop App

A modular, lightweight World Clock desktop application built with Python and Tkinter using standard library `zoneinfo`.

## Project Structure

```text
├── main.py        # Application entry point and Tkinter UI logic
├── styles.py      # Color palette, font definitions, and ttk theme settings
├── timezones.py   # Supported IANA timezone dataset
└── README.md      # Documentation and run instructions
```

## Features

- **24-Hour Digital Clock (`00:00:00`)**: Displays both local time and selected timezone in a clean `HH:MM:SS` format.
- **Timezone Selection**: Pre-configured with major world timezones (including `America/New_York`, `Asia/Tokyo`, `Europe/London`, `Europe/Zurich`, `UTC`, etc.) stored in [timezones.py](file:///d:/Claude-project/claude03/timezones.py).
- **Accurate UTC Offset & DST**: Shows the real-time UTC offset (e.g. `UTC+02:00 (CEST)`) and relative time comparison (e.g. `(5 hrs behind local)`).
- **1-Second Synchronous Updates**: Both clocks update in real-time every second.
- **Centralized Styling**: All colors, fonts, and widget themes are cleanly isolated in [styles.py](file:///d:/Claude-project/claude03/styles.py).

## Requirements

- Python 3.9+ (includes standard `zoneinfo`)

## How to Run

Launch the application by running [main.py](file:///d:/Claude-project/claude03/main.py):

```bash
python main.py
```
