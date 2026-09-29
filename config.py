"""Configuration and settings manager for Spider Break Companion."""
from __future__ import annotations

import copy
import json
import os
import sys
import time
import winreg
from pathlib import Path

APP_NAME = "Spider Break Companion"
DATA_DIR = Path(os.environ.get("APPDATA", Path.home())) / "SpiderBreakCompanion"
CONFIG_FILE = DATA_DIR / "settings.json"

# Fresh installation defaults: ZERO active reminders by default!
DEFAULT_SETTINGS = {
    "first_launch": True,
    "legacy_migrated": True,  # True for new installs so legacy prompt never runs
    "pending_legacy_choice": False,
    "start_with_windows": False,
    "reduced_motion": False,
    "reminders": [],  # Empty list by default!
}


def get_default_settings() -> dict:
    """Return a fresh independent copy of default settings."""
    return copy.deepcopy(DEFAULT_SETTINGS)


def migrate_legacy_settings(saved: dict) -> dict:
    """Repeatably migrate legacy settings (eye_minutes, water_minutes, custom_reminders) to unified reminders format."""
    migrated = copy.deepcopy(saved)

    reminders = migrated.get("reminders")
    if not isinstance(reminders, list):
        reminders = []

    existing_ids = {r.get("id") for r in reminders if isinstance(r, dict)}

    # Check if legacy eye/water parameters exist and migration hasn't been finalized
    if not saved.get("legacy_migrated", False):
        has_legacy_eye = "eye_minutes" in saved and "legacy_eye" not in existing_ids
        has_legacy_water = "water_minutes" in saved and "legacy_water" not in existing_ids

        if has_legacy_eye:
            eye_min = max(1, min(180, int(saved["eye_minutes"])))
            reminders.append({
                "id": "legacy_eye",
                "title": "Eye Break",
                "message": "Look 20 feet away for 20 seconds",
                "schedule_type": "recurring",
                "interval_value": eye_min,
                "interval_unit": "minutes",
                "interval_minutes": eye_min,
                "enabled": False,  # Pending explicit user choice!
                "completed": False,
                "next_due_timestamp": time.time() + (eye_min * 60),
                "snoozed_until": 0.0,
                "is_template": False,
            })

        if has_legacy_water:
            water_min = max(15, min(360, int(saved["water_minutes"])))
            reminders.append({
                "id": "legacy_water",
                "title": "Hydration Break",
                "message": "Time to drink water",
                "schedule_type": "recurring",
                "interval_value": water_min,
                "interval_unit": "minutes",
                "interval_minutes": water_min,
                "enabled": False,  # Pending explicit user choice!
                "completed": False,
                "next_due_timestamp": time.time() + (water_min * 60),
                "snoozed_until": 0.0,
                "is_template": False,
            })

        # Preserve existing custom_reminders array if present
        legacy_custom = saved.get("custom_reminders", [])
        if isinstance(legacy_custom, list):
            for c_rem in legacy_custom:
                if isinstance(c_rem, dict):
                    c_id = c_rem.get("id") or f"rem_{int(time.time() * 1000)}"
                    if c_id not in existing_ids:
                        due_ts = float(c_rem.get("due_timestamp", 0))
                        completed = bool(c_rem.get("completed", False))
                        reminders.append({
                            "id": c_id,
                            "title": c_rem.get("title", "Custom Reminder"),
                            "message": c_rem.get("message", ""),
                            "schedule_type": "once",
                            "due_timestamp": due_ts,
                            "due_datetime_iso": c_rem.get("due_datetime_iso", ""),
                            "enabled": not completed,
                            "completed": completed,
                            "snoozed_until": 0.0,
                        })
                        existing_ids.add(c_id)

        if has_legacy_eye or has_legacy_water:
            migrated["pending_legacy_choice"] = True

    migrated["reminders"] = reminders
    return migrated


def load_settings() -> dict:
    """Load settings from JSON, running migration if needed, falling back to clean defaults."""
    try:
        if CONFIG_FILE.exists():
            saved = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                return migrate_legacy_settings(saved)
    except Exception:
        pass
    return get_default_settings()


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
