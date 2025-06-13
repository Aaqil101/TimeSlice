# ----- Build-In Modules -----
import sys
from pathlib import Path

import pyperclip

plugindir: Path = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

# ----- Flow Launcher Modules -----
from flowlauncher import FlowLauncher

# ----- Configurable Constants -----
AppIcon: Path = Path(__file__).parent / "Assets" / "app.ico"
InfoIcon: Path = Path(__file__).parent / "Assets" / "info.ico"
WarningIcon: Path = Path(__file__).parent / "Assets" / "warning.ico"


class TimeSlice(FlowLauncher):
    def query(self, query: str):
        try:
            parts: list[int] = list(map(int, query.strip().split(":")))
            if len(parts) == 2:
                h, m = parts
                s = 0
            elif len(parts) == 3:
                h, m, s = parts
            else:
                raise ValueError

            total_hours: float = h + m / 60 + s / 3600
            rounded_hours: float = round(total_hours, 2)

            result_text: str = f"{rounded_hours}"
            pyperclip.copy(result_text)

            return [
                {
                    "Title": f"{query.strip()} → {result_text} hrs",
                    "SubTitle": "Copied to clipboard",
                    "IcoPath": str(InfoIcon),
                    "JsonRPCAction": {
                        "method": "copy",
                        "parameters": [result_text],
                        "dontHideAfterAction": False,
                    },
                }
            ]
        except Exception:
            return [
                {
                    "Title": "Invalid time format",
                    "SubTitle": "Use HH:MM or HH:MM:SS (e.g. 1:45 or 01:30:00)",
                    "IcoPath": str(WarningIcon),
                }
            ]

    def copy(self, text: str) -> None:
        pyperclip.copy(text)


if __name__ == "__main__":
    TimeSlice()
