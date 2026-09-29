"""Reminder timing and queueing engine for Spider Break Companion.

Supports recurring Eye and Water breaks as well as One-Time Custom Reminders
with overdue detection, single-fire completion, and in-place snooze rescheduling.
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

        # Recurring timers for eye and water breaks
        self.eye_timer = QTimer(self)
        self.eye_timer.timeout.connect(lambda: self.on_interval_due("eye"))

        self.water_timer = QTimer(self)
        self.water_timer.timeout.connect(lambda: self.on_interval_due("water"))

        # Checking timer for custom one-time reminders (every 1 second)
        self.custom_timer = QTimer(self)
        self.custom_timer.timeout.connect(self.check_custom_reminders)
        self.custom_timer.start(1000)

        self.start_timers()

        # Check for overdue reminders on launch
        QTimer.singleShot(1500, self.check_custom_reminders)

    def start_timers(self):
        """Start or restart recurring timers based on current settings."""
        if self.paused:
            return

        eye_ms = self.settings.get("eye_minutes", 20) * 60 * 1000
        water_ms = self.settings.get("water_minutes", 120) * 60 * 1000

        self.eye_timer.start(eye_ms)
        self.water_timer.start(water_ms)

    def stop_timers(self):
        """Stop all running timers."""
        self.eye_timer.stop()
        self.water_timer.stop()

    def update_settings(self, new_settings: dict):
        """Update settings and restart interval timers."""
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
        """Triggered automatically when a recurring reminder timer fires."""
        if self.paused:
            return
        self.request_break(kind)

    def check_custom_reminders(self):
        """Check scheduled custom reminders and trigger due/overdue reminders."""
        if self.paused:
            return

        custom_list = self.settings.get("custom_reminders", [])
        now = time.time()

        for rem in custom_list:
            if rem.get("completed", False):
                continue

            due_ts = rem.get("due_timestamp", 0)
            if now >= due_ts:
                # Check if reminder became due while app was closed / laptop asleep
                is_overdue = due_ts < (self.startup_timestamp - 10)
                rem_data = {
                    "id": rem.get("id"),
                    "title": rem.get("title", "Custom Reminder"),
                    "message": rem.get("message", ""),
                    "is_overdue": is_overdue,
                    "due_timestamp": due_ts,
                }
                self.request_break("custom", rem_data)
                break  # Trigger one custom break at a time, rest will queue

    def request_break(self, kind: str, custom_data: Optional[dict] = None):
        """Request a break. If another break is active, queue it without duplicates."""
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
        """Snooze a break for specified minutes. Modifies custom reminders in-place."""
        if kind == "custom" and custom_data and custom_data.get("id"):
            rem_id = custom_data.get("id")
            new_due_ts = time.time() + (minutes * 60)
            # Update reminder in settings in-place
            custom_list = self.settings.get("custom_reminders", [])
            for rem in custom_list:
                if rem.get("id") == rem_id:
                    rem["due_timestamp"] = new_due_ts
                    rem["completed"] = False
                    break
            save_settings(self.settings)

        self.on_break_finished(completed=False)

        if kind != "custom":
            snooze_ms = minutes * 60 * 1000
            QTimer.singleShot(snooze_ms, lambda: self.request_break(kind, custom_data))

    def mark_custom_completed(self, custom_data: dict):
        """Mark custom reminder completed so it never fires again."""
        if not custom_data or not custom_data.get("id"):
            return
        rem_id = custom_data.get("id")
        custom_list = self.settings.get("custom_reminders", [])
        for rem in custom_list:
            if rem.get("id") == rem_id:
                rem["completed"] = True
                break
        save_settings(self.settings)

    def on_break_finished(self, completed: bool = True):
        """Called when active break window completes or is dismissed."""
        # Done and automatic timeout complete a reminder; Snooze keeps it pending.
        if completed and self.active_break and self.active_break["kind"] == "custom":
            self.mark_custom_completed(self.active_break["custom_data"])

        self.active_break = None
        # Process next queued break if any
        if self.queue:
            next_item = self.queue.popleft()
            QTimer.singleShot(500, lambda: self.request_break(next_item["kind"], next_item["custom_data"]))

    def trigger_test(self, kind: str, custom_data: Optional[dict] = None):
        """Immediately trigger a test break."""
        item = {"kind": kind, "custom_data": custom_data or {}}
        if self.active_break is not None:
            self.queue.append(item)
            return
        self.active_break = item
        self.trigger_callback(kind, custom_data)
