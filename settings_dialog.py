"""Settings and Reminder Manager dialog for Spider Break Companion."""
from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Callable, Optional

from PyQt5.QtCore import QDate, QDateTime, QTime, Qt
from PyQt5.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
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
    QRadioButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from config import save_settings, set_autostart


class SettingsDialog(QDialog):
    """Reminder Manager and Settings dialog for Spider Break Companion."""

    def __init__(
        self,
        settings: dict,
        on_save_callback: Callable[[dict], None],
        on_test_animation_callback: Callable[[], None],
        parent=None,
    ):
        super().__init__(parent)
        self.settings = settings
        self.on_save_callback = on_save_callback
        self.on_test_animation_callback = on_test_animation_callback

        self.editing_reminder_id: Optional[str] = None

        self.setWindowTitle("Spidey Reminder Manager")
        self.setFixedWidth(620)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        # Title Header
        title = QLabel("🕷  Spidey Reminder Manager", self)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0F172A;")
        main_layout.addWidget(title)

        # First Launch Welcome Banner if no reminders set
        if self.settings.get("first_launch", False) or not self.settings.get("reminders"):
            self.banner = QWidget(self)
            self.banner.setStyleSheet("""
                QWidget {
                    background-color: #EFF6FF;
                    border: 1px solid #BFDBFE;
                    border-radius: 8px;
                    padding: 8px;
                }
            """)
            b_layout = QVBoxLayout(self.banner)
            b_layout.setContentsMargins(12, 10, 12, 10)
            b_text = QLabel(
                "✨ <b>Welcome!</b> Add your first reminder below, or pick a template (Eye Break / Hydration) to get started.",
                self.banner,
            )
            b_text.setWordWrap(True)
            b_text.setStyleSheet("color: #1E40AF; font-size: 13px;")
            b_layout.addWidget(b_text)
            main_layout.addWidget(self.banner)

        # 1. Add / Edit Reminder Form Group
        form_group = QGroupBox("Add / Edit Reminder", self)
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(10)

        # Template Selection Row
        template_row = QHBoxLayout()
        tpl_label = QLabel("Optional Template:", form_group)
        tpl_label.setStyleSheet("font-weight: 600; color: #475569;")
        template_row.addWidget(tpl_label)

        self.tpl_combo = QComboBox(form_group)
        self.tpl_combo.addItem("-- Choose a template to autofill... --", None)
        self.tpl_combo.addItem("👁 Eye Break (Repeating every 20 minutes)", "eye")
        self.tpl_combo.addItem("💧 Hydration Break (Repeating every 2 hours)", "water")
        self.tpl_combo.currentIndexChanged.connect(self.on_template_selected)
        template_row.addWidget(self.tpl_combo, stretch=1)
        form_layout.addLayout(template_row)

        form = QFormLayout()
        form.setSpacing(8)

        self.title_input = QLineEdit(form_group)
        self.title_input.setPlaceholderText("e.g. Call Rahul, Eye Break, or Team Meeting")
        form.addRow("Reminder Title *:", self.title_input)

        self.message_input = QLineEdit(form_group)
        self.message_input.setPlaceholderText("e.g. Look 20 feet away for 20 seconds (optional)")
        form.addRow("Optional Message:", self.message_input)

        # Schedule Type Selection (Radio Buttons)
        type_row = QHBoxLayout()
        self.radio_once = QRadioButton("One-Time Schedule", form_group)
        self.radio_recurring = QRadioButton("Repeating Schedule", form_group)
        self.radio_once.setChecked(True)

        self.type_group = QButtonGroup(self)
        self.type_group.addButton(self.radio_once)
        self.type_group.addButton(self.radio_recurring)
        self.radio_once.toggled.connect(self.toggle_schedule_type_ui)

        type_row.addWidget(self.radio_once)
        type_row.addWidget(self.radio_recurring)
        type_row.addStretch()
        form.addRow("Schedule Type:", type_row)

        # One-Time Schedule Container
        self.once_container = QWidget(form_group)
        once_layout = QHBoxLayout(self.once_container)
        once_layout.setContentsMargins(0, 0, 0, 0)
        once_layout.setSpacing(8)

        now_dt = datetime.now() + timedelta(minutes=15)
        self.date_edit = QDateEdit(QDate(now_dt.year, now_dt.month, now_dt.day), self.once_container)
        self.date_edit.setCalendarPopup(True)
        once_layout.addWidget(self.date_edit)

        self.time_edit = QTimeEdit(QTime(now_dt.hour, now_dt.minute), self.once_container)
        once_layout.addWidget(self.time_edit)

        local_lbl = QLabel("(Computer's Local Time)", self.once_container)
        local_lbl.setStyleSheet("color: #64748B; font-size: 11px;")
        once_layout.addWidget(local_lbl)
        once_layout.addStretch()

        form.addRow("Date & Time *:", self.once_container)

        # Repeating Schedule Container
        self.recurring_container = QWidget(form_group)
        rec_layout = QHBoxLayout(self.recurring_container)
        rec_layout.setContentsMargins(0, 0, 0, 0)
        rec_layout.setSpacing(8)

        rec_lbl = QLabel("Repeat every:", self.recurring_container)
        rec_layout.addWidget(rec_lbl)

        self.spin_interval = QSpinBox(self.recurring_container)
        self.spin_interval.setRange(1, 999)
        self.spin_interval.setValue(20)
        rec_layout.addWidget(self.spin_interval)

        self.unit_combo = QComboBox(self.recurring_container)
        self.unit_combo.addItem("Minutes", "minutes")
        self.unit_combo.addItem("Hours", "hours")
        rec_layout.addWidget(self.unit_combo)
        rec_layout.addStretch()

        form.addRow("Repeat Interval *:", self.recurring_container)
        self.recurring_container.hide()

        form_layout.addLayout(form)

        # Form Action Buttons Row
        btn_form_row = QHBoxLayout()
        self.btn_save_rem = QPushButton("Save Reminder", form_group)
        self.btn_save_rem.setStyleSheet("""
            QPushButton {
                background: #2563EB;
                color: white;
                border-radius: 6px;
                padding: 7px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1D4ED8;
            }
        """)
        self.btn_save_rem.clicked.connect(self.handle_save_reminder)
        btn_form_row.addWidget(self.btn_save_rem)

        self.btn_cancel_edit = QPushButton("Cancel Edit", form_group)
        self.btn_cancel_edit.hide()
        self.btn_cancel_edit.clicked.connect(self.reset_form_inputs)
        btn_form_row.addWidget(self.btn_cancel_edit)

        btn_test_anim = QPushButton("🕷 Test Animation", form_group)
        btn_test_anim.setToolTip("Preview entrance animation (does not save a reminder)")
        btn_test_anim.setStyleSheet("""
            QPushButton {
                background: #F1F5F9;
                color: #334155;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 7px 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #E2E8F0;
            }
        """)
        btn_test_anim.clicked.connect(self.on_test_animation_callback)
        btn_form_row.addWidget(btn_test_anim)

        btn_form_row.addStretch()
        form_layout.addLayout(btn_form_row)

        main_layout.addWidget(form_group)

        # 2. Saved Reminders Table Group
        list_group = QGroupBox("Your Reminders", self)
        list_layout = QVBoxLayout(list_group)
        list_layout.setSpacing(8)

        self.table = QTableWidget(list_group)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title & Message", "Schedule Details", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setMinimumHeight(160)

        list_layout.addWidget(self.table)
        main_layout.addWidget(list_group)

        # 3. Preferences Group
        pref_group = QGroupBox("App Preferences", self)
        pref_layout = QVBoxLayout(pref_group)
        pref_layout.setSpacing(6)

        self.startup_check = QCheckBox("Start with Windows automatically", pref_group)
        self.startup_check.setChecked(bool(self.settings.get("start_with_windows", False)))
        pref_layout.addWidget(self.startup_check)

        self.reduced_motion_check = QCheckBox("Enable reduced motion (skip entrance animations)", pref_group)
        self.reduced_motion_check.setChecked(bool(self.settings.get("reduced_motion", False)))
        pref_layout.addWidget(self.reduced_motion_check)

        main_layout.addWidget(pref_group)

        # Footer Dialog Action Row
        footer_row = QHBoxLayout()
        footer_row.addStretch()

        btn_close = QPushButton("Close", self)
        btn_close.setDefault(True)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: white;
                border-radius: 6px;
                padding: 7px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1E293B;
            }
        """)
        btn_close.clicked.connect(self.save_preferences_and_close)
        footer_row.addWidget(btn_close)

        main_layout.addLayout(footer_row)

        self.refresh_table()

    def toggle_schedule_type_ui(self):
        """Toggle visibility between One-Time and Repeating schedule inputs."""
        if self.radio_once.isChecked():
            self.once_container.show()
            self.recurring_container.hide()
        else:
            self.once_container.hide()
            self.recurring_container.show()

    def on_template_selected(self, index: int):
        """Autofill form from selected template without saving automatically."""
        tpl_key = self.tpl_combo.currentData()
        if not tpl_key:
            return

        if tpl_key == "eye":
            self.title_input.setText("Eye Break")
            self.message_input.setText("Look 20 feet away for 20 seconds")
            self.radio_recurring.setChecked(True)
            self.spin_interval.setValue(20)
            self.unit_combo.setCurrentIndex(0)  # minutes
        elif tpl_key == "water":
            self.title_input.setText("Hydration Break")
            self.message_input.setText("Time to drink water")
            self.radio_recurring.setChecked(True)
            self.spin_interval.setValue(2)
            self.unit_combo.setCurrentIndex(1)  # hours

    def handle_save_reminder(self):
        """Validate input and save/update reminder in settings."""
        title = self.title_input.text().strip()
        msg = self.message_input.text().strip()

        if not title:
            QMessageBox.critical(self, "Title Required", "Please enter a title for your reminder.")
            return

        is_once = self.radio_once.isChecked()
        reminders = self.settings.get("reminders", [])

        if is_once:
            qdate = self.date_edit.date()
            qtime = self.time_edit.time()
            dt = datetime(qdate.year(), qdate.month(), qdate.day(), qtime.hour(), qtime.minute(), qtime.second())
            ts = dt.timestamp()

            if ts <= time.time() and not self.editing_reminder_id:
                QMessageBox.critical(
                    self,
                    "Invalid Time",
                    "Scheduled date and time must be in the future (computer's local time).",
                )
                return

            rem_dict = {
                "id": self.editing_reminder_id or f"rem_{int(time.time() * 1000)}",
                "title": title,
                "message": msg,
                "schedule_type": "once",
                "due_timestamp": ts,
                "due_datetime_iso": dt.isoformat(),
                "enabled": True,
                "completed": False,
            }
        else:
            val = self.spin_interval.value()
            unit = self.unit_combo.currentData()
            total_min = val if unit == "minutes" else val * 60

            rem_dict = {
                "id": self.editing_reminder_id or f"rem_{int(time.time() * 1000)}",
                "title": title,
                "message": msg,
                "schedule_type": "recurring",
                "interval_value": val,
                "interval_unit": unit,
                "interval_minutes": total_min,
                "enabled": True,
                "completed": False,
                "next_due_timestamp": time.time() + (total_min * 60),
                "snoozed_until": 0.0,
            }

        if self.editing_reminder_id:
            for idx, r in enumerate(reminders):
                if r.get("id") == self.editing_reminder_id:
                    reminders[idx] = rem_dict
                    break
        else:
            reminders.append(rem_dict)

        self.settings["reminders"] = reminders
        self.settings["first_launch"] = False
        save_settings(self.settings)

        self.reset_form_inputs()
        self.refresh_table()
        self.on_save_callback(self.settings)

    def reset_form_inputs(self):
        self.editing_reminder_id = None
        self.title_input.clear()
        self.message_input.clear()
        self.tpl_combo.setCurrentIndex(0)
        self.radio_once.setChecked(True)
        self.btn_save_rem.setText("Save Reminder")
        self.btn_cancel_edit.hide()

        now_dt = datetime.now() + timedelta(minutes=15)
        self.date_edit.setDate(QDate(now_dt.year, now_dt.month, now_dt.day))
        self.time_edit.setTime(QTime(now_dt.hour, now_dt.minute))

    def refresh_table(self):
        """Refresh saved reminders table."""
        reminders = self.settings.get("reminders", [])
        self.table.setRowCount(len(reminders))

        now = time.time()

        for row, rem in enumerate(reminders):
            # Column 0: Title & Message
            t_text = rem.get("title", "")
            m_text = rem.get("message", "")
            full_txt = f"{t_text}\n({m_text})" if m_text else t_text
            self.table.setItem(row, 0, QTableWidgetItem(full_txt))

            # Column 1: Schedule Details
            stype = rem.get("schedule_type", "once")
            if stype == "once":
                ts = rem.get("due_timestamp", 0)
                sched_txt = f"Once: {datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')}"
            else:
                val = rem.get("interval_value", rem.get("interval_minutes", 20))
                unit = rem.get("interval_unit", "minutes")
                sched_txt = f"Every {val} {unit}"
            self.table.setItem(row, 1, QTableWidgetItem(sched_txt))

            # Column 2: Status Badge
            enabled = rem.get("enabled", False)
            completed = rem.get("completed", False)

            if completed:
                status_txt = "Completed"
                color = Qt.gray
            elif not enabled:
                status_txt = "Disabled"
                color = Qt.gray
            elif stype == "once" and rem.get("due_timestamp", 0) < now:
                status_txt = "Overdue"
                color = Qt.red
            else:
                status_txt = "Active"
                color = Qt.darkGreen

            s_item = QTableWidgetItem(status_txt)
            s_item.setForeground(color)
            self.table.setItem(row, 2, s_item)

            # Column 3: Action Buttons (Edit, Enable/Disable, Delete)
            act_widget = QWidget()
            act_layout = QHBoxLayout(act_widget)
            act_layout.setContentsMargins(4, 2, 4, 2)
            act_layout.setSpacing(6)

            btn_edit = QPushButton("Edit", act_widget)
            btn_edit.setStyleSheet("padding: 2px 6px; font-size: 11px;")
            btn_edit.clicked.connect(lambda _, r=rem: self.edit_reminder(r))
            act_layout.addWidget(btn_edit)

            btn_toggle = QPushButton("Disable" if enabled else "Enable", act_widget)
            btn_toggle.setStyleSheet("padding: 2px 6px; font-size: 11px;")
            btn_toggle.clicked.connect(lambda _, r_id=rem.get("id"): self.toggle_reminder(r_id))
            act_layout.addWidget(btn_toggle)

            btn_del = QPushButton("Delete", act_widget)
            btn_del.setStyleSheet("padding: 2px 6px; font-size: 11px; color: #DC2626;")
            btn_del.clicked.connect(lambda _, r_id=rem.get("id"): self.delete_reminder(r_id))
            act_layout.addWidget(btn_del)

            self.table.setCellWidget(row, 3, act_widget)

    def edit_reminder(self, rem: dict):
        """Populate form fields for editing an existing reminder."""
        self.editing_reminder_id = rem.get("id")
        self.title_input.setText(rem.get("title", ""))
        self.message_input.setText(rem.get("message", ""))

        stype = rem.get("schedule_type", "once")
        if stype == "once":
            self.radio_once.setChecked(True)
            ts = rem.get("due_timestamp", time.time())
            dt = datetime.fromtimestamp(ts)
            self.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
            self.time_edit.setTime(QTime(dt.hour, dt.minute))
        else:
            self.radio_recurring.setChecked(True)
            self.spin_interval.setValue(rem.get("interval_value", 20))
            unit = rem.get("interval_unit", "minutes")
            self.unit_combo.setCurrentIndex(0 if unit == "minutes" else 1)

        self.btn_save_rem.setText("Update Reminder")
        self.btn_cancel_edit.show()

    def toggle_reminder(self, rem_id: str):
        """Toggle enabled/disabled state for a reminder."""
        reminders = self.settings.get("reminders", [])
        for rem in reminders:
            if rem.get("id") == rem_id:
                rem["enabled"] = not rem.get("enabled", False)
                if rem["enabled"] and rem.get("schedule_type") == "recurring":
                    rem["next_due_timestamp"] = time.time() + (rem.get("interval_minutes", 20) * 60)
                break
        save_settings(self.settings)
        self.refresh_table()
        self.on_save_callback(self.settings)

    def delete_reminder(self, rem_id: str):
        """Delete a reminder after confirmation."""
        reminders = self.settings.get("reminders", [])
        self.settings["reminders"] = [r for r in reminders if r.get("id") != rem_id]
        save_settings(self.settings)

        if self.editing_reminder_id == rem_id:
            self.reset_form_inputs()
        self.refresh_table()
        self.on_save_callback(self.settings)

    def save_preferences_and_close(self):
        """Save startup and reduced motion preferences and close dialog."""
        startup = self.startup_check.isChecked()
        try:
            set_autostart(startup)
        except OSError as exc:
            QMessageBox.warning(self, "Startup Setting Error", str(exc))

        self.settings.update({
            "start_with_windows": startup,
            "reduced_motion": self.reduced_motion_check.isChecked(),
            "first_launch": False,
        })
        save_settings(self.settings)
        self.on_save_callback(self.settings)
        self.accept()
