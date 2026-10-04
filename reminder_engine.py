"""Reminder timing and queueing engine for Spider Break Companion.

Supports recurring Eye, Water, and Custom reminders with overdue detection,
interval rescheduling, snooze handling, and queue management.
"""
from __future__ import annotations

import time
from collections import deque
from typing import Callable, Optional
from PyQt5.QtCore import QObject, QTimer

from config import save_settings


class ReminderEngine(QObject):

    def __init__(
        self,
        settings: dict,
        trigger_callback: Callable[[str, Optional[dict]], None],
    ):
        super().__init__()
        self.settings = settings
        self.trigger_callback = trigger_callback
        self.paused = False
        self.active_break: Optional[dict] = None  # {"kind": str, "custom_data": dict}
        self.queue: deque[dict] = deque()

        self.startup_timestamp = time.time()

        # Core checking timer (runs every 1 second)
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_reminders)
        self.check_timer.start(1000)

        # Legacy timers for backwards compatibility if legacy settings are active
        self.eye_timer = QTimer(self)
        self.eye_timer.timeout.connect(lambda: self.on_interval_due("eye"))
        self.water_timer = QTimer(self)
        self.water_timer.timeout.connect(lambda: self.on_interval_due("water"))

        self.start_timers()

        # Check for due/overdue reminders on launch
        QTimer.singleShot(1500, self.check_reminders)

    def start_timers(self):
        """Start interval checking and legacy timers based on current settings."""
        if self.paused:
            return

        if not self.check_timer.isActive():
            self.check_timer.start(1000)

        # Legacy fallback timers if eye_minutes / water_minutes are explicitly set in settings
        if "eye_minutes" in self.settings:
            eye_ms = self.settings.get("eye_minutes", 20) * 60 * 1000
            self.eye_timer.start(eye_ms)
        if "water_minutes" in self.settings:
            water_ms = self.settings.get("water_minutes", 120) * 60 * 1000
            self.water_timer.start(water_ms)

    def stop_timers(self):
        """Stop all running timers."""
        self.check_timer.stop()
        self.eye_timer.stop()
        self.water_timer.stop()

    def update_settings(self, new_settings: dict):
        """Update settings and restart timers."""
        self.settings = new_settings
        self.stop_timers()
        if not self.paused:
            self.start_timers()

    def set_paused(self, paused: bool):
        """Pause or resume the reminder engine."""
        self.paused = paused
        if paused:
            self.stop_timers()
        else:
            self.start_timers()

    def on_interval_due(self, kind: str):
        """Triggered automatically when a legacy recurring timer fires."""
        if self.paused:
            return
        self.request_break(kind)

    def check_reminders(self):
        """Check all scheduled reminders (unified reminders & legacy custom_reminders)."""
        if self.paused:
            return

        now = time.time()
        reminders = self.settings.get("reminders", [])

        # Fallback to legacy custom_reminders if unified list is empty
        if not reminders:
            reminders = self.settings.get("custom_reminders", [])

        for rem in reminders:
            if not isinstance(rem, dict):
                continue

            if not rem.get("enabled", True) or rem.get("completed", False):
                continue

            # Check snooze deadline
            snoozed_until = float(rem.get("snoozed_until", 0.0))
            if now < snoozed_until:
                continue

            stype = rem.get("schedule_type", "once")

            if stype == "once":
                due_ts = float(rem.get("due_timestamp", 0.0))
                if due_ts > 0 and now >= due_ts:
                    is_overdue = due_ts < (self.startup_timestamp - 10)
                    rem_data = {
                        "id": rem.get("id"),
                        "title": rem.get("title", "Custom Reminder"),
                        "message": rem.get("message", ""),
                        "is_overdue": is_overdue,
                        "due_timestamp": due_ts,
                    }
                    self.request_break("custom", rem_data)
                    break  # Fire one due reminder per tick; remainder will queue

            elif stype == "recurring":
                next_due = float(rem.get("next_due_timestamp", 0.0))
                interval_min = int(rem.get("interval_minutes", rem.get("interval_value", 20)))
                interval_sec = max(60, interval_min * 60)

                # Initialize next_due if zero or invalid
                if next_due <= 0:
                    rem["next_due_timestamp"] = now + interval_sec
                    save_settings(self.settings)
                    continue

                if now >= next_due:
                    # Reschedule next occurrence into the future
                    rem["next_due_timestamp"] = now + interval_sec
                    rem["snoozed_until"] = 0.0
                    save_settings(self.settings)

                    rem_data = {
                        "id": rem.get("id"),
                        "title": rem.get("title", "Reminder"),
                        "message": rem.get("message", ""),
                        "is_overdue": False,
                    }
                    self.request_break("custom", rem_data)
                    break

    def check_custom_reminders(self):
        """Backward-compatibility alias for check_reminders."""
        self.check_reminders()

    def request_break(self, kind: str, custom_data: Optional[dict] = None):
        """Request a break overlay. Queue without duplicate if an overlay is currently active."""
        item = {"kind": kind, "custom_data": custom_data or {}}

        if self.active_break is not None:
            # Check if identical item is already queued
            is_queued = False
            for q in self.queue:
                if q["kind"] == kind:
                    if kind == "custom":
                        if q["custom_data"].get("id") == item["custom_data"].get("id"):
                            is_queued = True
                    else:
                        is_queued = True

            if not is_queued and item != self.active_break:
                self.queue.append(item)
            return

        self.active_break = item
        self.trigger_callback(kind, custom_data)

    def snooze_break(self, kind: str, custom_data: Optional[dict] = None, minutes: int = 5):
        """Snooze a break for specified minutes. Updates snoozed_until timestamp in settings."""
        if custom_data and custom_data.get("id"):
            rem_id = custom_data.get("id")
            new_snooze_until = time.time() + (minutes * 60)

            # Update in settings.json
            for rlist in [self.settings.get("reminders", []), self.settings.get("custom_reminders", [])]:
                for rem in rlist:
                    if isinstance(rem, dict) and rem.get("id") == rem_id:
                        rem["snoozed_until"] = new_snooze_until
                        save_settings(self.settings)
                        break

        self.on_break_finished(completed=False)

        if kind != "custom":
            snooze_ms = minutes * 60 * 1000
            QTimer.singleShot(snooze_ms, lambda: self.request_break(kind, custom_data))

    def mark_custom_completed(self, custom_data: dict):
        """Mark one-time custom reminder completed so it does not fire again."""
        if not custom_data or not custom_data.get("id"):
            return
        rem_id = custom_data.get("id")

        for rlist in [self.settings.get("reminders", []), self.settings.get("custom_reminders", [])]:
            for rem in rlist:
                if isinstance(rem, dict) and rem.get("id") == rem_id:
                    if rem.get("schedule_type") == "once":
                        rem["completed"] = True
                        rem["enabled"] = False
                        save_settings(self.settings)
                    break

    def on_break_finished(self, completed: bool = True):
        """Called when active break overlay closes or is dismissed."""
        if completed and self.active_break and self.active_break["kind"] == "custom":
            self.mark_custom_completed(self.active_break["custom_data"])

        self.active_break = None
        # Process next queued break if any
        if self.queue:
            next_item = self.queue.popleft()
            QTimer.singleShot(500, lambda: self.request_break(next_item["kind"], next_item["custom_data"]))

    def trigger_test(self, kind: str, custom_data: Optional[dict] = None):
        """Immediately trigger a test break overlay."""
        item = {"kind": kind, "custom_data": custom_data or {}}
        if self.active_break is not None:
            self.queue.append(item)
            return
        self.active_break = item
        self.trigger_callback(kind, custom_data)
