"""Configuration and settings manager for Spider Break Companion."""
from __future__ import annotations

import json
import os
import sys
import winreg
from pathlib import Path

APP_NAME = "Spider Break Companion"
DATA_DIR = Path(os.environ.get("APPDATA", Path.home())) / "SpiderBreakCompanion"
CONFIG_FILE = DATA_DIR / "settings.json"

DEFAULTS = {
    "eye_minutes": 20,
    "water_minutes": 120,
    "start_with_windows": False,
    "reduced_motion": False,
    "custom_reminders": [],
}


def load_settings() -> dict:
    """Load settings from JSON, falling back to defaults if invalid."""
    try:
        if CONFIG_FILE.exists():
            saved = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            result = DEFAULTS | {k: saved[k] for k in DEFAULTS if k in saved}
            result["eye_minutes"] = max(1, min(180, int(result["eye_minutes"])))
            result["water_minutes"] = max(15, min(360, int(result["water_minutes"])))
            if not isinstance(result["custom_reminders"], list):
                result["custom_reminders"] = []
            return result
    except Exception:
        pass
    return DEFAULTS.copy()


def save_settings(settings: dict) -> None:
    """Save settings dictionary to JSON atomically."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp = CONFIG_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    temp.replace(CONFIG_FILE)


def set_autostart(enabled: bool) -> None:
    """Enable or disable Windows startup via CurrentUser Run key."""
    if sys.platform != "win32":
        return

    if getattr(sys, "frozen", False):
        command = f'"{sys.executable}"'
    else:
        main_script = Path(__file__).parent / "companion.py"
        pythonw = Path(sys.executable).with_name("pythonw.exe")
        exe = pythonw if pythonw.exists() else sys.executable
        command = f'"{exe}" "{main_script.resolve()}"'

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE,
        ) as key:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, command)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
    except Exception as exc:
        raise OSError(f"Failed to update startup registry: {exc}") from exc
