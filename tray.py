"""System tray manager for Spider Break Companion."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap, QPolygon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

TRAY_ICON_PATH = Path(__file__).parent / "tray_icon.png"


def create_default_tray_icon() -> QIcon:
    """Generate a clean spider tray icon pixmap if icon file does not exist."""
    if TRAY_ICON_PATH.exists():
        return QIcon(str(TRAY_ICON_PATH))

    # Draw a 32x32 spider mask icon programmatically
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Red circular mask background
    painter.setBrush(QColor("#EF4444"))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(2, 2, 28, 28)

    # White spider eyes
    painter.setBrush(QColor("#FFFFFF"))
    # Left eye
    painter.drawPolygon(
        QPolygon([QPoint(8, 12), QPoint(14, 14), QPoint(14, 20), QPoint(9, 18)])
    )
    # Right eye
    painter.drawPolygon(
        QPolygon([QPoint(24, 12), QPoint(18, 14), QPoint(18, 20), QPoint(23, 18)])
    )
    painter.end()

    try:
        pixmap.save(str(TRAY_ICON_PATH))
    except Exception:
        pass

    return QIcon(pixmap)


class TrayManager:
    """System tray icon manager with context menu for break companion."""

    def __init__(
        self,
        on_test_eye: Callable[[], None],
        on_test_water: Callable[[], None],
        on_toggle_pause: Callable[[], bool],
        on_open_settings: Callable[[], None],
        on_quit: Callable[[], None],
    ):
        self.on_test_eye = on_test_eye
        self.on_test_water = on_test_water
        self.on_toggle_pause = on_toggle_pause
        self.on_open_settings = on_open_settings
        self.on_quit = on_quit

        self.tray = QSystemTrayIcon(create_default_tray_icon())
        self.tray.setToolTip("Spider Break Companion")

        self.menu = QMenu()
        self.init_menu()

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.on_tray_activated)

    def init_menu(self):
        # Test eye break
        action_eye = QAction("👁  Test eye break", self.menu)
        action_eye.triggered.connect(self.on_test_eye)
        self.menu.addAction(action_eye)

        # Test water break
        action_water = QAction("💧  Test water reminder", self.menu)
        action_water.triggered.connect(self.on_test_water)
        self.menu.addAction(action_water)

        self.menu.addSeparator()

        # Pause / Resume
        self.pause_action = QAction("⏸  Pause reminders", self.menu)
        self.pause_action.triggered.connect(self.handle_pause_toggle)
        self.menu.addAction(self.pause_action)

        # Settings
        action_settings = QAction("⚙  Settings...", self.menu)
        action_settings.triggered.connect(self.on_open_settings)
        self.menu.addAction(action_settings)

        self.menu.addSeparator()

        # Quit
        action_quit = QAction("❌  Quit", self.menu)
        action_quit.triggered.connect(self.on_quit)
        self.menu.addAction(action_quit)

    def handle_pause_toggle(self):
        """Toggle pause state and update menu action text."""
        is_paused = self.on_toggle_pause()
        if is_paused:
            self.pause_action.setText("▶  Resume reminders")
            self.tray.setToolTip("Spider Break Companion (Paused)")
        else:
            self.pause_action.setText("⏸  Pause reminders")
            self.tray.setToolTip("Spider Break Companion")

    def on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
        """Handle single or double click on tray icon."""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.on_open_settings()

    def show(self):
        self.tray.show()

    def cleanup(self):
        """Hide and delete system tray icon cleanly on exit."""
        self.tray.hide()
        self.tray.deleteLater()
