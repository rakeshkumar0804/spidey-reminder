"""Settings dialog for Spider Break Companion.

Supports configuring recurring break intervals, autostart, reduced-motion animation options,
and managing One-Time Custom Reminders (add, edit, delete, inline validation).
"""
from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Callable, Optional

from PyQt5.QtCore import QDate, QDateTime, QTime, Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from config import save_settings, set_autostart


class SettingsDialog(QDialog):
    """Settings dialog for break companion intervals, startup, animations, and custom reminders."""

    def __init__(
        self,
        settings: dict,
        on_save_callback: Callable[[dict], None],
        on_test_callback: Callable[[str, Optional[dict]], None],
        parent=None,
    ):
        super().__init__(parent)
        self.settings = settings
        self.on_save_callback = on_save_callback
        self.on_test_callback = on_test_callback

        self.editing_reminder_id: Optional[str] = None

        self.setWindowTitle("Spider Break Companion Settings")
        self.setFixedWidth(540)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        title = QLabel("🕷  Spider Break Companion Settings", self)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0F172A;")
        main_layout.addWidget(title)

        # 1. Recurring Reminders & Preferences Group
        rec_group = QGroupBox("Recurring Breaks & Preferences", self)
        rec_layout = QFormLayout(rec_group)
        rec_layout.setSpacing(10)

        self.eye_input = QLineEdit(str(self.settings.get("eye_minutes", 20)), rec_group)
        self.eye_input.setFixedWidth(70)
        rec_layout.addRow("Eye break interval (minutes):", self.eye_input)

        self.water_input = QLineEdit(str(self.settings.get("water_minutes", 120)), rec_group)
        self.water_input.setFixedWidth(70)
        rec_layout.addRow("Water break interval (minutes):", self.water_input)

        self.startup_check = QCheckBox("Start with Windows", rec_group)
        self.startup_check.setChecked(bool(self.settings.get("start_with_windows", False)))
        rec_layout.addRow("", self.startup_check)

        self.reduced_motion_check = QCheckBox("Enable reduced motion (skip entrance animations)", rec_group)
        self.reduced_motion_check.setChecked(bool(self.settings.get("reduced_motion", False)))
        rec_layout.addRow("", self.reduced_motion_check)

        main_layout.addWidget(rec_group)

        # 2. Custom Reminders Group
        custom_group = QGroupBox("Custom One-Time Reminders", self)
        custom_layout = QVBoxLayout(custom_group)
        custom_layout.setSpacing(10)

        form = QFormLayout()
        form.setSpacing(8)

        self.title_input = QLineEdit(custom_group)
        self.title_input.setPlaceholderText("e.g. Call Rahul or Project meeting")
        form.addRow("Reminder Title *:", self.title_input)

        self.message_input = QLineEdit(custom_group)
        self.message_input.setPlaceholderText("e.g. Discuss project timeline (optional)")
        form.addRow("Optional Message:", self.message_input)

        # Date & Time Pickers (Local computer time)
        picker_row = QHBoxLayout()
        now_dt = datetime.now() + timedelta(minutes=10)

        self.date_edit = QDateEdit(QDate(now_dt.year, now_dt.month, now_dt.day), custom_group)
        self.date_edit.setCalendarPopup(True)
        picker_row.addWidget(self.date_edit)

        self.time_edit = QTimeEdit(QTime(now_dt.hour, now_dt.minute), custom_group)
        picker_row.addWidget(self.time_edit)

        local_label = QLabel("(Computer's Local Time)", custom_group)
        local_label.setStyleSheet("color: #64748B; font-size: 11px;")
        picker_row.addWidget(local_label)

        form.addRow("Scheduled Time *:", picker_row)
        custom_layout.addLayout(form)

        # Add / Update Reminder Button
        btn_row = QHBoxLayout()
        self.btn_add_custom = QPushButton("Add Custom Reminder", custom_group)
        self.btn_add_custom.setStyleSheet("""
            QPushButton {
                background: #2563EB;
                color: white;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1D4ED8;
            }
        """)
        self.btn_add_custom.clicked.connect(self.handle_add_or_update_reminder)
        btn_row.addWidget(self.btn_add_custom)

        self.btn_cancel_edit = QPushButton("Cancel Edit", custom_group)
        self.btn_cancel_edit.hide()
        self.btn_cancel_edit.clicked.connect(self.reset_custom_inputs)
        btn_row.addWidget(self.btn_cancel_edit)

        btn_row.addStretch()
        custom_layout.addLayout(btn_row)

        # Table of Upcoming Reminders
        self.table = QTableWidget(custom_group)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Scheduled Local Time", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setMinimumHeight(140)

        custom_layout.addWidget(self.table)
        main_layout.addWidget(custom_group)

        self.refresh_table()

        # 3. Test Buttons & Save Row
        action_group = QHBoxLayout()

        btn_test_eye = QPushButton("Test Eye Break", self)
        btn_test_eye.clicked.connect(lambda: self.on_test_callback("eye", None))
        action_group.addWidget(btn_test_eye)

        btn_test_water = QPushButton("Test Water Break", self)
        btn_test_water.clicked.connect(lambda: self.on_test_callback("water", None))
        action_group.addWidget(btn_test_water)

        action_group.addStretch()

        btn_cancel = QPushButton("Cancel", self)
        btn_cancel.clicked.connect(self.reject)
        action_group.addWidget(btn_cancel)

        btn_save = QPushButton("Save Settings", self)
        btn_save.setDefault(True)
        btn_save.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: white;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1E293B;
            }
        """)
        btn_save.clicked.connect(self.save)
        action_group.addWidget(btn_save)

        main_layout.addLayout(action_group)

    def handle_add_or_update_reminder(self):
        """Validate input and add/update a custom one-time reminder."""
        title = self.title_input.text().strip()
        msg = self.message_input.text().strip()

        if not title:
            QMessageBox.critical(self, "Invalid Title", "Please enter a title for the custom reminder.")
            return

        qdate = self.date_edit.date()
        qtime = self.time_edit.time()
        dt = datetime(qdate.year(), qdate.month(), qdate.day(), qtime.hour(), qtime.minute(), qtime.second())
        ts = dt.timestamp()

        # Reject past times unless editing
        if ts <= time.time():
            QMessageBox.critical(
                self,
                "Invalid Scheduled Time",
                "Scheduled time must be in the future (computer's local time).",
            )
            return

        custom_list = self.settings.get("custom_reminders", [])

        if self.editing_reminder_id:
            # Update existing reminder
            for rem in custom_list:
                if rem.get("id") == self.editing_reminder_id:
                    rem["title"] = title
                    rem["message"] = msg
                    rem["due_timestamp"] = ts
                    rem["due_datetime_iso"] = dt.isoformat()
                    rem["completed"] = False
                    break
        else:
            # Add new reminder
            new_id = f"rem_{int(time.time() * 1000)}"
            custom_list.append({
                "id": new_id,
                "title": title,
                "message": msg,
                "due_timestamp": ts,
                "due_datetime_iso": dt.isoformat(),
                "completed": False,
            })

        self.settings["custom_reminders"] = custom_list
        save_settings(self.settings)
        self.reset_custom_inputs()
        self.refresh_table()

    def reset_custom_inputs(self):
        self.editing_reminder_id = None
        self.title_input.clear()
        self.message_input.clear()
        self.btn_add_custom.setText("Add Custom Reminder")
        self.btn_cancel_edit.hide()

        now_dt = datetime.now() + timedelta(minutes=10)
        self.date_edit.setDate(QDate(now_dt.year, now_dt.month, now_dt.day))
        self.time_edit.setTime(QTime(now_dt.hour, now_dt.minute))

    def refresh_table(self):
        """Refresh the upcoming custom reminders table."""
        custom_list = self.settings.get("custom_reminders", [])
        # Filter uncompleted reminders
        pending = [r for r in custom_list if not r.get("completed", False)]
        pending.sort(key=lambda x: x.get("due_timestamp", 0))

        self.table.setRowCount(len(pending))

        for row, rem in enumerate(pending):
            self.table.setItem(row, 0, QTableWidgetItem(rem.get("title", "")))

            ts = rem.get("due_timestamp", 0)
            dt_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
            self.table.setItem(row, 1, QTableWidgetItem(dt_str))

            is_overdue = ts < time.time()
            status_text = "Overdue" if is_overdue else "Pending"
            status_item = QTableWidgetItem(status_text)
            if is_overdue:
                status_item.setForeground(Qt.red)
            self.table.setItem(row, 2, status_item)

            # Action buttons widget
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(6)

            btn_edit = QPushButton("Edit", action_widget)
            btn_edit.setStyleSheet("padding: 2px 8px; font-size: 11px;")
            btn_edit.clicked.connect(lambda _, r=rem: self.edit_reminder(r))
            action_layout.addWidget(btn_edit)

            btn_del = QPushButton("Delete", action_widget)
            btn_del.setStyleSheet("padding: 2px 8px; font-size: 11px; color: #DC2626;")
            btn_del.clicked.connect(lambda _, r_id=rem.get("id"): self.delete_reminder(r_id))
            action_layout.addWidget(btn_del)

            self.table.setCellWidget(row, 3, action_widget)

    def edit_reminder(self, rem: dict):
        """Populate form fields for editing an existing custom reminder."""
        self.editing_reminder_id = rem.get("id")
        self.title_input.setText(rem.get("title", ""))
        self.message_input.setText(rem.get("message", ""))

        ts = rem.get("due_timestamp", time.time())
        dt = datetime.fromtimestamp(ts)
        self.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        self.time_edit.setTime(QTime(dt.hour, dt.minute))

        self.btn_add_custom.setText("Update Custom Reminder")
        self.btn_cancel_edit.show()

    def delete_reminder(self, rem_id: str):
        """Delete a custom reminder after confirmation."""
        custom_list = self.settings.get("custom_reminders", [])
        self.settings["custom_reminders"] = [r for r in custom_list if r.get("id") != rem_id]
        save_settings(self.settings)
        if self.editing_reminder_id == rem_id:
            self.reset_custom_inputs()
        self.refresh_table()

    def save(self):
        """Validate recurring interval inputs and save settings."""
        try:
            eye_min = int(self.eye_input.text().strip())
            water_min = int(self.water_input.text().strip())

            if not (1 <= eye_min <= 180):
                raise ValueError("Eye break interval must be between 1 and 180 minutes.")
            if not (15 <= water_min <= 360):
                raise ValueError("Water break interval must be between 15 and 360 minutes.")

        except ValueError as err:
            QMessageBox.critical(self, "Invalid Interval", str(err))
            return

        startup = self.startup_check.isChecked()
        try:
            set_autostart(startup)
        except OSError as exc:
            QMessageBox.warning(self, "Startup Error", str(exc))

        self.settings.update({
            "eye_minutes": eye_min,
            "water_minutes": water_min,
            "start_with_windows": startup,
            "reduced_motion": self.reduced_motion_check.isChecked(),
        })

        save_settings(self.settings)
        self.on_save_callback(self.settings)
        self.accept()
