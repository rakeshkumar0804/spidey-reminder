"""Spider Break Companion - Main Application Entry Point.

Includes Windows Named Mutex single-instance protection, clean system tray icon
destruction on quit, and robust queueing integration with the overlay state machine.
"""
from __future__ import annotations

import ctypes
import sys
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import QApplication

from config import load_settings
from overlay import OverlayState, SpiderOverlayWindow
from reminder_engine import ReminderEngine
from settings_dialog import SettingsDialog
from tray import TrayManager

# Windows Single-Instance Mutex
MUTEX_NAME = "SpiderBreakCompanion_SingleInstance_Mutex"


def ensure_single_instance() -> bool:
    """Enforce single instance on Windows using a named system mutex."""
    if sys.platform != "win32":
        return True
    try:
        kernel32 = ctypes.windll.kernel32
        mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
        last_error = kernel32.GetLastError()
        if last_error == 183:  # ERROR_ALREADY_EXISTS
            return False
        return True
    except Exception:
        return True


class BreakCompanionApp:
    """Main application manager for Spider Break Companion."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("Spider Break Companion")

        # Load persisted settings
        self.settings = load_settings()

        # Active overlay and settings dialog handles
        self.active_overlay: Optional[SpiderOverlayWindow] = None
        self.settings_dialog: Optional[SettingsDialog] = None

        # Initialize core reminder engine
        self.engine = ReminderEngine(self.settings, self.trigger_break)

        # Initialize system tray icon and menu
        self.tray = TrayManager(
            on_test_eye=lambda: self.engine.trigger_test("eye"),
            on_test_water=lambda: self.engine.trigger_test("water"),
            on_toggle_pause=self.toggle_pause,
            on_open_settings=self.open_settings,
            on_quit=self.quit,
        )
        self.tray.show()

    def toggle_pause(self) -> bool:
        """Toggle pause state in reminder engine and return new state."""
        new_state = not self.engine.paused
        self.engine.set_paused(new_state)
        return new_state

    def trigger_break(self, kind: str, custom_data: Optional[dict] = None):
        """Callback from reminder engine when a break is due or tested."""
        if (
            self.active_overlay is not None
            and self.active_overlay.state != OverlayState.HIDDEN
        ):
            # An overlay is currently active or exiting; queue break
            item = {"kind": kind, "custom_data": custom_data or {}}
            if item not in self.engine.queue:
                self.engine.queue.append(item)
            return

        def on_done():
            self.active_overlay = None
            self.engine.on_break_finished()

        def on_snooze():
            self.active_overlay = None
            self.engine.snooze_break(kind, custom_data=custom_data, minutes=5)

        reduced_motion_pref = bool(self.settings.get("reduced_motion", False))

        overlay = SpiderOverlayWindow(
            kind,
            on_done=on_done,
            on_snooze=on_snooze,
            custom_data=custom_data,
            # Pass False explicitly: an unchecked app setting must play the
            # entrance even if Windows has disabled its own UI animations.
            force_reduced_motion=reduced_motion_pref,
        )
        self.active_overlay = overlay
        overlay.start_sequence()

    def open_settings(self):
        """Open or focus the settings dialog."""
        if self.settings_dialog is not None and self.settings_dialog.isVisible():
            self.settings_dialog.raise_()
            self.settings_dialog.activateWindow()
            return

        dialog = SettingsDialog(
            settings=self.settings,
            on_save_callback=self.on_settings_saved,
            on_test_callback=self.engine.trigger_test,
        )
        self.settings_dialog = dialog
        dialog.show()

    def on_settings_saved(self, new_settings: dict):
        """Callback when settings are updated and saved."""
        self.settings = new_settings
        self.engine.update_settings(new_settings)

    def quit(self):
        """Clean application exit: stop timers, hide tray icon, close overlay."""
        self.engine.stop_timers()
        if self.active_overlay is not None:
            self.active_overlay.close()
        self.tray.cleanup()
        self.app.quit()

    def run(self) -> int:
        return self.app.exec_()


def main():
    if not ensure_single_instance():
        print("Spider Break Companion is already running.")
        sys.exit(0)

    app = BreakCompanionApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
