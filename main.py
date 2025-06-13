# ----- Build-In Modules -----
import sys
from pathlib import Path
from typing import Any, Dict

import pyperclip

plugindir: Path = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

# ----- Py Flow Launcher Modules -----
from pyflowlauncher import Plugin, ResultResponse, send_results
from pyflowlauncher.result import JsonRPCAction, Result
from pyflowlauncher.settings import settings

# ----- Configurable Constants -----
AppIcon: Path = Path(__file__).parent / "src" / "app.png"
DEFAULT_DECIMAL_PLACES = "2"

# Initialize plugin
plugin = Plugin()


def convert_time(query: str, settings_dict: Dict[str, Any]) -> ResultResponse:
    """
    Converts a time string in "HH:MM" or "HH:MM:SS" format to a decimal hour representation.
    Args:
        query (str): A string representing the time, formatted as "HH:MM" or "HH:MM:SS".
        settings_dict (Dict[str, Any]): Dictionary containing plugin settings
    Returns:
        ResultResponse: The converted time wrapped in a ResultResponse object.
    Raises:
        ValueError: If the input string does not match the expected format.
    """
    parts: list[int] = list(map(int, query.strip().split(":")))
    if len(parts) == 2:
        h, m = parts
        s = 0
    elif len(parts) == 3:
        h, m, s = parts
    else:
        raise ValueError

    total_hours: float = h + m / 60 + s / 3600
    # Get decimal places from settings, convert to int, and clamp between 0 and 6
    decimal_places: int = min(
        6, max(0, int(settings_dict.get("decimal_places", DEFAULT_DECIMAL_PLACES)))
    )
    result: str = f"{round(total_hours, decimal_places)}"

    # Create the formatted display string showing input → result
    display_text: str = f"{query.strip()} → {result} hrs"

    # Create result with action
    time_result = Result(
        Title=display_text, SubTitle="Press Enter to copy", IcoPath=str(AppIcon)
    )
    time_result.add_action(copy, [result])

    return send_results([time_result])


@plugin.on_method
def copy(text: str) -> None:
    """Copy text to clipboard
    Args:
        text (str): The text to copy
    """
    pyperclip.copy(text)


@plugin.on_method
def query(query: str) -> ResultResponse:
    try:
        # Check for empty input
        if not query.strip():
            empty_result = Result(
                Title="Enter time in HH:MM or HH:MM:SS format",
                SubTitle="Example: 1:30 or 1:30:15",
                IcoPath=str(AppIcon),
            )
            return send_results([empty_result])

        # Get current settings
        plugin_settings: Dict[str, Any] = settings()
        return convert_time(query, plugin_settings)

    except ValueError:
        error_result = Result(
            Title="Invalid time format",
            SubTitle="Please enter time in HH:MM or HH:MM:SS format",
            IcoPath=str(AppIcon),
        )
        return send_results([error_result])


if __name__ == "__main__":
    plugin.run()
