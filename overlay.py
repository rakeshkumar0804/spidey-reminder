"""Overlay window for Spider-Man break companion.

Features a movie-like 6-stage entrance animation sequence:
1. WEB SHOT: Thin web shoots downward from top edge over 550 ms (Spider-Man & card hidden).
2. WEB HOLD: Hold web strand alone for 200 ms.
3. SPIDER-MAN DESCENT: Visibly descends from above screen over 1,400 ms attached to strand.
4. SETTLE: Small damped hanging motion + pause for 400 ms.
5. CARD OPEN: Open empty reminder card over 400 ms (heading visible, sentence hidden).
6. WORD REVEAL: Reveal sentence WORD BY WORD at 300 ms per word.
7. ACTIVE: Every reminder counts down for 20 seconds, then exits automatically.

Clean character transparency, separate application-rendered web strand, Win32 focus protection,
and screen bounds constraint.
"""
from __future__ import annotations

import ctypes
import base64
import math
import time
import re
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Optional

from PyQt5.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QRectF,
    QTimer,
    Qt,
    pyqtProperty,
)
from PyQt5.QtGui import (
    QColor,
    QCursor,
    QFont,
    QFontMetrics,
    QGuiApplication,
    QPainter,
    QPen,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

ASSET_PATH = Path(__file__).parent / "spiderman_hanging.png"

# User-supplied twisted web artwork, cut out and embedded to keep the repository layout.
WEB_TEXTURE_PNG = (
    b"iVBORw0KGgoAAAANSUhEUgAAABsAAABzCAYAAABpc3liAAAM/0lEQVR4nLWaWXBVx5nHf1/3ufdquQgtIARIbGIxBtksBhswRmGC"
    b"F1Jje4jHVcnDzJPLL1M18zRv8zjPU3lPxfEk5XLGntjxFqewXTi22QLGZhMCCwkhBMYIofUu53R/83CucFIT6R7pKl0l3Zdz+tdf"
    b"99dff9+/jwwMDDBdMxQIGFNf6OU//vPnvPjTf+eVX73Gf/3sZ+QKIW+99guaawY5+KN9hCzFUSeOzAz9zdA8KRy1kkrXsra9lRuD"
    b"/aSCgInJHAgIigdAZuomGQwMSkAQBOzb0cHVc2d5YP1ajh89Cj4CjQisRRHQimHxqJ0LaG9fw52hPrZt38Jbv/0t6cBibYBgwEcY"
    b"cWV5CWDxoG2qyM7dm7hypYsVK9o4dvQkqJBOpwkkwjCG4CqHGSAIlPXrl/PHTz/ln/75p7zxxm8oFop4Fbwqhohyc5kApngEEUhZ"
    b"T3d3N5cudrF3zx7e/t07QIANLJKgs7Iwj8FTg3fVqFM2rF/P2++8w4EfdtK6fAVOBRdqIn9MNI2ejHiqwXka6ut44cf/yGuvv8FL"
    b"L7/EF18cwwQG0QhKG6EiWImIx+Aix57dT/DtrdssqGsglclyrfcq1kwgzAwsC5t6wOOx4hETgFgOPHOAd37/PgcPvcQrrx0jpA4h"
    b"r3YGR0lumQEjIAigbHxwI4Pf3mb9xge5NnCX4bFxjOYw5OZu2f0HBRCJ3xCoqaolW5ulr+8GrW0ruX59ECnjJcktu98EI4IYC2r4"
    b"5nIva9es5VrfNcCBD7XyaQTEGASInBJ5jw1S9PRcpalpMcNDQxidxEph2vdnbdnUjgoIsCbF3eFRMlVVTE4WELS0BeYJBsQnigkQ"
    b"Y4nCCO80Dsg6c5fBXDgoqPc452hetJix0XEaGhtxksVJDdOdb4ktU8CILXmcx0VFRCNWrWrhxq1rtCxtxIugpKf1ycQw+YtfT2CF"
    b"Qn6Cjo7N3Lx5nbZVrajGm79i2BRJxGBsQBiGjI2P09KyiOGhG7Q0N4FUoVTNB8zEmzpOPrh6rY+WJY1cuXSKDe1LSKcsnio86XmA"
    b"eY8VgxVD5EKOHjvG47t38cnh9/lh504MGg/k/l8lMAOIYKwQhiFdl7ppXtREd9dJNnWsxqgicVCbu2X3A48HjKCqnDh+goce6uBC"
    b"1zl2796GUYenCsWWHW9ZmKGgNiiC9+RyeY4cOUJnZyfvvfcuO7Z24NXgqcVXCjMoxucRP4kRR09PF3V1WUaGb9PT3Y1qERNU4aUW"
    b"KoUBGBMHcmsyqHhefPHHfPjBRzy+53F85HDRTLvr+5YgXCliQgye/oE7dGx+mLAYIcawfPkyAmMRW4qLlZ1nHsFj/CRhWOSDD4/y"
    b"3D+8wAfvvc+hQ4cQgchHoD5Ruj8DzBMwSYrbKtYxcHOcoREllakhlw9Zu2YVIkIQBKDzUFgYJjVlhvCqHP7kK/7+2Rc4fvRPPP/8"
    b"IZz7M0Ay1swwAYwIY+NFTpzqYd0DD3H23AU2bFiLTwiYBSxCXZ4vv7zA2ge2c/ZsF3e+G6ZQnLmAmANMMRRwRHx+/DJPPvkMJ098"
    b"Tk1NCmMsCDivszo2/uqzhogUOQwRo6OOgZt5GuoXMj52i9qadJxdKTjnIYji+nPuxaDHkFdDRPeVXhoaF3O15zLLli4C8WiCjmcB"
    b"KyFVudh1je3bdvD1V1+yfdsG8A6XJFzMHmYYHByhfd1a+vt7aF/TgroQazwKqIvPuHkp4CPvmMg5arP1FAqTLKg1oJ7IxWtUKBYJ"
    b"UmmkXN6dBKYqhM4i1pIKLBnjIIqwNs4QFEVMIt8oDwu9AwJELClrsAEYG1sXD0YxCWWJsjD1gFhEFEEQUVIWfMlD1HuMNUmj1cww"
    b"a1L4sIjBk8sXUHEYE+fyXoTIRVRlMok39swwa/CugHMhxTDEmCqKCQ/KWcMCozQ0VDE6OoqYNMMjxbJJzZxhIp7FjdWMDA+Rrsly"
    b"ZygH5s+SUJ0qeyuATb1ujad1eQNXv7lMe/taenpvE4ax66mP1y4VpCrzRofBkxbFsq69la7zF9m6bTtff92NCabP5ecEg4CQWjxp"
    b"2tqaCF2O1uUruHFrmFSmCu994o2cAAYg4JXqtKV50QImcjnqsovJ50OgtLdK4T/pqT3zFlFDTQB7drRx5MhHPLH/Kfr6BvBhRKCg"
    b"OEzA/OQg3lRRpIbt2zfQdf4E27Y+RHPLEoqFIsjsJ7KMRpzGm1pqMvBIxzKudJ+lc9/jfPHFH0lsTiKYj9W4ULOkUwHPHtzGRx/+"
    b"L88/d5AP/3CYQrE4a9j06bcxOKqAOvGINjelWb+6ka++OsWzzz7H22+9He8xBHzFGTEoAZ5qPNVYEZ55ajsfvvc79u/v5Oz5cwzd"
    b"uUMxDBGTLBQneMoQsYAoqmVBNsVA71VOHD3Ooeef5+y5cxgR1CXLIxNJ7Z4sPshiMCzI1vD+B++yeXMHmzseouAsxiiB5KhYSVUE"
    b"T0acZnAI2fp6tmzZwqkzp9l/4BDvvnseTIBhFJhet0oEi9ddVbBgDTYIOPjMU3x8+DA7d27l5J++IixGGJkoye0VwOKJSYtKgAvj"
    b"W4kFdfWsWLmKb3r62dvZyZkzF2IlgWJJtp0jDAwh1TipxaRSuChCvWffE/v4+JOP2fd3T/LeHz4lDBXLREm2nbO4KYBF1SAIiuLV"
    b"07a8lbvDwzQ1NfPdnUlyeYOiVKR+f9/0PkwVvHqcj7h0uYeVqzfTN/BdSfh00wbNWUmAMXAqbzR4hFNnzrJ63SYudfcCeQy5krRU"
    b"iWVTM+Q9SCyaZdIZenp6aW1bRf/1QayJMBSnncjESqoI2JQiouSdA6t48YxPjtNQ38jI0BhWp7Nptpb9RfN4D6nAogrWZlCNk7y/"
    b"AYyS58XShAlSOOdwKjNGrDnDDELkQjKZDNbGJa9OqdXzARMVbBDgfVyVIgb1impEEASoOmaSHGdv2X2tXUE9qUyKiYkJUkGAlSl/"
    b"++vWzVrXnyKKUdKZDJl0mnv3RqhvqCfWuu6P6P+1Oa8ZwMTEJM3NLdwcvE1bWxvOKUowbaeziyDiMQGI9xix5HPw4LqN9HSfpn11"
    b"I0qmlEZUCLsPxCMenAupymRYt24dt29fZ9XKJagYPCmpcBqVUn0ExNEqny9icQTkMJpnYX22rBKY6J7akidgEpXvJ6jr4iUefngT"
    b"Z04fY++jD2NVUWrwc/1qIm4e4wugecRHWGMpFAuc/foMe/fs4Nhnv2fv3q0oHke1xLnmHKfRlP4ZBRWDMYZCocidO0OoK5DLfcvi"
    b"xXV4MmiZnZRwzbyW7hAA4fDhj3h8z27Onz3N/r07Sx8wCOUEwdl5o8LY6CinT53mkUd28sXnR+h8Yhfq8yDlNYSEsCmboJCL2Lq1"
    b"g1s3B+jrG8CYCK8W5xeU7a58kqogRGqNIwoNLlR+dPBpjh09Sk1VLam0gqnGUU3FNxYiiiWHlSL9/XdZ1LyMmmwNXZe6aG1txVpb"
    b"OttgHr4HiTNH9cqJk93sP3CAjz/5hEd37iAIgpLrJKtCE21qBfKhcP5iPxs2dvDZp5+xb18nhUIe1VLGNT8wjzUFhoaGEJtlaHiU"
    b"mtqFLMhmARCR+dEbv+eFXLnUy4r2ds5dvMwTe/ehRvDT56Nzh6kXeq59y8rV7Zw4eYo1a9rBeVQ1aYWbHOYUhu5NUruglr7eXpx4"
    b"nEDk4quupCpFsmkUw0QhxJoUk5PjOI3wJoYBJWectwgCKQsuEgTB+DjTmm0rD1OwxtBYv4CReyM0NjaQqaqeNSgZDBCrLF1Wz9Dt"
    b"QZY2N1MVZPDq8T4ukhLK+glgYvAuYMvmDfT1dbFp43oi51BV1PvEnpgMRqxhLV/WjIZDDA7eQGWqMARM8luEhGWukrKeH+zbwsmT"
    b"J0il0tzPilE0oe8nzq4CC7se20TrskZUHd5rSZyuTbxoiT85FHHUpB2LGjIYa/BquDs8ybUbYzi1lQtlcROcVhO5AJX4/kUVEOHe"
    b"yAi//O/XMVaxOg9ykgecZHBajfOK9z5WClzEkpZl9PbdZGJ8AiP5ymH3mwo6dVB6jyAsXFjPI4/s53J3f6KuZpXwTF1fxaKBo+CU"
    b"nY/u4ty5yyimbGdzr6nVY4yhadFS7t7Lx975t4IVC0WqqmsJQ6WmKotgysb92dXUpVBh8IyNjtOyqIlbN/tpW74Ea8p3llBv9CoS"
    b"Z4WijrCQ5ze/fp0Xnn2a45/9D3t2r0S0vHSbEGZEVSki5AtFXn311+x+bDfjk2OMjQ6xsK4Br8H8fCENIEZQL4xM5FhYt5Cnn+nk"
    b"1Vd+wb/9678gthpnspVXMVOLrl4oFAxNTS289PLL/PyXv6Kr+zzZbAaHwyc4uZPVZ/FxzYXL11m5Zh2fff453kesXr2cdCa+1VUJ"
    b"xM9PyaSqDi6cu8Li5qW8+eab/OQnLyBG8VEelQye2rL3oclFFxGKkWf42zs8tmsXXgxRVCBVFVAkwPmg7Nj/D8k5wQ9oaqKeAAAA"
    b"AElFTkSuQmCC"
)
REMINDER_SECONDS = 20

# Win32 Constants for non-activating topmost window
GWL_EXSTYLE = -20
WS_EX_NOACTIVATE = 0x08000000
WS_EX_TOPMOST = 0x00000008
WS_EX_TOOLWINDOW = 0x00000080
SPI_GETCLIENTAREAANIMATION = 0x1010

# Exact Requested Animation Timing Constants (in milliseconds)
WEB_SHOOT_MS = 550
WEB_HOLD_MS = 200
SPIDEY_DESCENT_MS = 1400
SETTLE_MS = 350
SETTLE_PAUSE_MS = 400
CARD_OPEN_MS = 400
WORD_INTERVAL_MS = 300
PUNCTUATION_PAUSE_MS = 450
EXIT_CARD_MS = 250
ASCEND_MS = 700
RETRACT_WEB_MS = 350


def is_reduced_motion_enabled() -> bool:
    """Check if Windows user has disabled animations / enabled reduced motion."""
    try:
        enabled = ctypes.c_bool()
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_GETCLIENTAREAANIMATION, 0, ctypes.byref(enabled), 0
        )
        return not enabled.value
    except Exception:
        return False


def apply_non_activating_flags(hwnd: int):
    """Ensure the overlay window never steals keyboard focus."""
    if not hwnd:
        return
    try:
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_NOACTIVATE | WS_EX_TOPMOST | WS_EX_TOOLWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    except Exception:
        pass


class OverlayState(Enum):
    HIDDEN = auto()
    SHOOTING_WEB = auto()
    HOLDING_WEB = auto()
    DESCENDING = auto()
    SETTLING = auto()
    CARD_OPENING = auto()
    REVEALING_WORDS = auto()
    ACTIVE = auto()
    EXITING_CARD = auto()
    ASCENDING = auto()
    RETRACTING_WEB = auto()


class MessageCardWidget(QWidget):
    """Clean message card matching the baseline target UI with red corner accents."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(280)
        self.setMinimumHeight(170)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Card rectangle with subtle inset for shadow/border
        r = self.rect().adjusted(2, 2, -2, -2)

        # Draw white background card
        painter.setBrush(QColor("#FFFFFF"))
        painter.setPen(QPen(QColor("#CBD5E1"), 1))
        painter.drawRoundedRect(r, 10, 10)

        # Draw 4 red corner accents
        painter.setBrush(QColor("#EF4444"))
        painter.setPen(Qt.NoPen)
        cs = 6  # Corner accent size

        # Top-left
        painter.drawRect(r.left(), r.top(), cs, cs)
        # Top-right
        painter.drawRect(r.right() - cs + 1, r.top(), cs, cs)
        # Bottom-left
        painter.drawRect(r.left(), r.bottom() - cs + 1, cs, cs)
        # Bottom-right
        painter.drawRect(r.right() - cs + 1, r.bottom() - cs + 1, cs, cs)


class SpiderOverlayWindow(QWidget):
    """State-machine driven transparent overlay for Spider-Man break companion."""

    def __init__(
        self,
        kind: str,
        on_done: Callable[[], None],
        on_snooze: Callable[[], None],
        custom_data: Optional[dict] = None,
        force_reduced_motion: Optional[bool] = None,
    ):
        super().__init__(
            flags=Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )
        self.kind = kind
        self.custom_data = custom_data or {}
        self.on_done_cb = on_done
        self.on_snooze_cb = on_snooze

        self.state = OverlayState.HIDDEN
        if force_reduced_motion is not None:
            self.reduced_motion = force_reduced_motion
        else:
            self.reduced_motion = is_reduced_motion_enabled()

        # Animation progress values
        self._web_progress = 0.0  # 0.0 to 1.0 (shooting / retracting web strand)
        self._spidey_y_offset = -350  # Vertical position offset of Spider-Man
        self.spidey_target_y_offset = 125
        self._pending_timers = []
        self._active_deadline = None
        self.web_texture = QPixmap()
        self.web_texture.loadFromData(base64.b64decode(WEB_TEXTURE_PNG), "PNG")

        # Persistent Animation objects
        self.anim_web: Optional[QPropertyAnimation] = None
        self.anim_spidey: Optional[QPropertyAnimation] = None
        self.anim_card: Optional[QPropertyAnimation] = None

        # Text reveal state
        self.full_sentence = self.get_full_sentence()
        self.words = self.full_sentence.split(" ") if self.full_sentence else []
        self.current_word_idx = 0
        self.word_timer: Optional[QTimer] = None

        # Countdown timer state
        self.remaining_seconds = REMINDER_SECONDS
        self.countdown_timer: Optional[QTimer] = None

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

        self.init_ui()

    def get_full_sentence(self) -> str:
        """Determine full sentence text based on reminder kind."""
        if self.kind == "eye":
            return "Look 20 feet away for 20 seconds"
        elif self.kind == "water":
            return "Time to drink water"
        elif self.kind == "custom":
            msg = self.custom_data.get("message", "").strip()
            return msg if msg else "Time for your scheduled reminder!"
        return ""

    def showEvent(self, event):
        super().showEvent(event)
        apply_non_activating_flags(int(self.winId()))

    # Property for web strand progress animation
    def get_web_progress(self) -> float:
        return self._web_progress

    def set_web_progress(self, val: float):
        self._web_progress = val
        self.update()

    web_progress = pyqtProperty(float, get_web_progress, set_web_progress)

    # Property for Spider-Man vertical offset animation
    def get_spidey_y_offset(self) -> int:
        return self._spidey_y_offset

    def set_spidey_y_offset(self, val: int):
        self._spidey_y_offset = val
        self.spidey_label.move(self.spidey_label.x(), self._spidey_y_offset)
        self.update()

    spidey_y_offset = pyqtProperty(int, get_spidey_y_offset, set_spidey_y_offset)

    def init_ui(self):
        # 1. Card Widget
        self.card = MessageCardWidget(self)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(8)

        # Drop shadow on card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setColor(QColor(0, 0, 0, 35))
        shadow.setOffset(0, 4)
        self.card.setGraphicsEffect(shadow)

        # Header tag ("■ EYE BREAK" / "■ HYDRATION" / "■ CUSTOM REMINDER")
        if self.kind == "eye":
            header_text = "■ EYE BREAK"
        elif self.kind == "water":
            header_text = "■ HYDRATION"
        elif self.kind == "custom":
            if self.custom_data.get("is_overdue"):
                header_text = "■ OVERDUE REMINDER"
            else:
                header_text = "■ CUSTOM REMINDER"
        else:
            header_text = "■ REMINDER"

        self.header_label = QLabel(header_text, self.card)
        self.header_label.setStyleSheet(
            "color: #EF4444; font-size: 11px; font-weight: bold; letter-spacing: 1px;"
        )
        card_layout.addWidget(self.header_label)

        # Title for Custom Reminder
        if self.kind == "custom":
            title_text = self.custom_data.get("title", "Custom Task")
            self.title_label = QLabel(title_text, self.card)
            self.title_label.setWordWrap(True)
            self.title_label.setStyleSheet(
                "color: #0F172A; font-size: 15px; font-weight: bold; line-height: 1.2;"
            )
            card_layout.addWidget(self.title_label)

        # Main prompt sentence (revealed word-by-word)
        self.msg_label = QLabel("", self.card)
        self.msg_label.setWordWrap(True)
        self.msg_label.setStyleSheet(
            "color: #334155; font-size: 13px; font-weight: 500; line-height: 1.3;"
        )
        card_layout.addWidget(self.msg_label)

        # Countdown shared by eye, water and custom reminders
        self.timer_label = QLabel("", self.card)
        self.timer_label.setStyleSheet(
            "color: #2563EB; font-size: 12px; font-weight: bold;"
        )
        self.timer_label.hide()
        card_layout.addWidget(self.timer_label)

        # Action Buttons Row
        self.btn_widget = QWidget(self.card)
        btn_row = QHBoxLayout(self.btn_widget)
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(10)

        self.btn_done = QPushButton("Done", self.btn_widget)
        self.btn_done.setCursor(Qt.PointingHandCursor)
        self.btn_done.setStyleSheet("""
            QPushButton {
                background-color: #0F172A;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 7px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E293B;
            }
        """)
        self.btn_done.clicked.connect(self.request_close)
        btn_row.addWidget(self.btn_done)

        self.btn_snooze = QPushButton("Snooze 5m", self.btn_widget)
        self.btn_snooze.setCursor(Qt.PointingHandCursor)
        self.btn_snooze.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #475569;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 7px 14px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #E2E8F0;
                color: #0F172A;
            }
        """)
        self.btn_snooze.clicked.connect(self.request_snooze)
        btn_row.addWidget(self.btn_snooze)

        card_layout.addWidget(self.btn_widget)
        self.btn_widget.hide()  # Hidden initially until word reveal finishes!

        # Hide card initially before Phase 5
        self.card.hide()

        # Spider-Man label
        self.spidey_label = QLabel(self)
        if ASSET_PATH.exists():
            pix = QPixmap(str(ASSET_PATH)).scaledToWidth(170, Qt.SmoothTransformation)
            self.spidey_label.setPixmap(pix)
            self.spidey_width = pix.width()
            self.spidey_height = pix.height()
        else:
            self.spidey_width = 150
            self.spidey_height = 290

        # Hide Spider-Man during Phase 1 (Web Shot)
        self.spidey_label.hide()

        self.spidey_label.resize(self.spidey_width, self.spidey_height)
        # Reserve the complete sentence's height before revealing individual words.
        self.msg_label.setTextFormat(Qt.PlainText)
        if self.kind == "custom":
            self.title_label.setTextFormat(Qt.PlainText)
        message_font = QFont("Segoe UI")
        message_font.setPixelSize(13)
        text_height = QFontMetrics(message_font).boundingRect(
            QRect(0, 0, 264, 10000), Qt.TextWordWrap, self.full_sentence
        ).height()
        self.msg_label.setMinimumHeight(text_height + 6)
        title_height = 0
        if self.kind == "custom":
            title_font = QFont("Segoe UI")
            title_font.setPixelSize(15)
            title_font.setBold(True)
            title_height = QFontMetrics(title_font).boundingRect(
                QRect(0, 0, 264, 10000), Qt.TextWordWrap,
                self.custom_data.get("title", "Custom Task")
            ).height() + 8
        card_width = 300
        card_height = max(195, text_height + title_height + 155)
        self.card.setFixedSize(card_width, card_height)
        spacing = 14

        self.overlay_width = card_width + spacing + self.spidey_width
        self.overlay_height = max(card_height + 155, self.spidey_height + self.spidey_target_y_offset + 20)
        self.resize(self.overlay_width, self.overlay_height)

        # Place card on left, Spider-Man on right
        self.card.move(0, 150)
        self.spidey_x = card_width + spacing
        self.spidey_label.move(self.spidey_x, -self.spidey_height)

        # Web strand anchor X relative to overlay
        self.web_anchor_x = self.spidey_x + int(self.spidey_width * 0.50)

    def paintEvent(self, event):
        """Paint thin white application-rendered web strand extending from top edge."""
        super().paintEvent(event)
        if self.state in (
            OverlayState.SHOOTING_WEB,
            OverlayState.HOLDING_WEB,
            OverlayState.DESCENDING,
            OverlayState.SETTLING,
            OverlayState.CARD_OPENING,
            OverlayState.REVEALING_WORDS,
            OverlayState.ACTIVE,
            OverlayState.EXITING_CARD,
            OverlayState.ASCENDING,
            OverlayState.RETRACTING_WEB,
        ):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # Reveal the supplied white web first; keep it anchored while the
            # character arrives, then retract it only after the character exits.
            full_web_height = self.spidey_target_y_offset + 10
            current_web_y = full_web_height
            if self.state in (OverlayState.SHOOTING_WEB, OverlayState.RETRACTING_WEB):
                current_web_y *= self._web_progress
            if current_web_y > 0:
                painter.setRenderHint(QPainter.SmoothPixmapTransform)
                painter.drawPixmap(
                    QRectF(self.web_anchor_x - 4, 0, 8, current_web_y),
                    self.web_texture,
                    QRectF(0, 0, self.web_texture.width(),
                           self.web_texture.height() * current_web_y / full_web_height),
                )

    def start_sequence(self):
        """Position window on active monitor and launch movie-like 6-stage sequence."""
        screen = (
            QGuiApplication.screenAt(QCursor.pos())
            if hasattr(QCursor, "pos")
            else None
        )
        if not screen:
            screen = QGuiApplication.primaryScreen()

        geom = screen.availableGeometry()

        right_margin = 30
        target_x = max(
            geom.x() + 10,
            geom.x() + geom.width() - self.overlay_width - right_margin,
        )
        target_y = geom.y()  # Attached to top screen edge of active monitor

        self.move(target_x, target_y)
        self.show()
        apply_non_activating_flags(int(self.winId()))

        if self.reduced_motion:
            self.jump_to_active_state()
        else:
            self.run_phase_1_web_shot()

    # --- Phase 1: Web Shot (550ms + 200ms hold) ---
    def run_phase_1_web_shot(self):
        self.state = OverlayState.SHOOTING_WEB
        self.spidey_label.hide()
        self.card.hide()
        self._web_progress = 0.0

        self.anim_web = QPropertyAnimation(self, b"web_progress", self)
        self.anim_web.setDuration(WEB_SHOOT_MS)
        self.anim_web.setStartValue(0.0)
        self.anim_web.setEndValue(1.0)
        self.anim_web.setEasingCurve(QEasingCurve.OutQuad)
        self.anim_web.finished.connect(self.run_phase_1_web_hold)
        self.anim_web.start()

    def run_phase_1_web_hold(self):
        self.state = OverlayState.HOLDING_WEB
        self._later(WEB_HOLD_MS, self.run_phase_2_spidey_descent)

    # --- Phase 2: Spider-Man Descent (1400ms) ---
    def run_phase_2_spidey_descent(self):
        self.state = OverlayState.DESCENDING
        self.spidey_label.show()  # Spider-Man becomes visible attached to web strand

        start_offset = -self.spidey_height
        target_offset = self.spidey_target_y_offset

        self.anim_spidey = QPropertyAnimation(self, b"spidey_y_offset", self)
        self.anim_spidey.setDuration(SPIDEY_DESCENT_MS)
        self.anim_spidey.setStartValue(start_offset)
        self.anim_spidey.setEndValue(target_offset)
        self.anim_spidey.setEasingCurve(QEasingCurve.OutCubic)

        self.anim_spidey.finished.connect(self.run_phase_3_settle)
        self.anim_spidey.start()

    # --- Phase 3: Settle (350ms damped motion + 400ms pause) ---
    def run_phase_3_settle(self):
        self.state = OverlayState.SETTLING

        # Small 3px damped hanging motion
        self.anim_settle = QPropertyAnimation(self, b"spidey_y_offset", self)
        self.anim_settle.setDuration(SETTLE_MS)
        self.anim_settle.setStartValue(self.spidey_target_y_offset)
        self.anim_settle.setEndValue(self.spidey_target_y_offset + 3)
        self.anim_settle.setEasingCurve(QEasingCurve.OutSine)

        def on_settle_down_done():
            # Settle back to 0
            self.anim_settle_up = QPropertyAnimation(self, b"spidey_y_offset", self)
            self.anim_settle_up.setDuration(SETTLE_MS)
            self.anim_settle_up.setStartValue(self.spidey_target_y_offset + 3)
            self.anim_settle_up.setEndValue(self.spidey_target_y_offset)
            self.anim_settle_up.setEasingCurve(QEasingCurve.InOutSine)
            self.anim_settle_up.finished.connect(
                lambda: self._later(SETTLE_PAUSE_MS, self.run_phase_4_card_open)
            )
            self.anim_settle_up.start()

        self.anim_settle.finished.connect(on_settle_down_done)
        self.anim_settle.start()

    # --- Phase 4: Card Open (400ms) ---
    def run_phase_4_card_open(self):
        self.state = OverlayState.CARD_OPENING
        self.card.show()

        # Attach QGraphicsOpacityEffect ONLY during card fade-in
        self.card_opacity = QGraphicsOpacityEffect(self.card)
        self.card.setGraphicsEffect(self.card_opacity)

        self.anim_card = QPropertyAnimation(self.card_opacity, b"opacity", self)
        self.anim_card.setDuration(CARD_OPEN_MS)
        self.anim_card.setStartValue(0.0)
        self.anim_card.setEndValue(1.0)
        self.anim_card.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_card.finished.connect(self.on_card_opened)
        self.anim_card.start()

    def on_card_opened(self):
        """Detach opacity effect after opening to prevent DWM flashing."""
        self.card.setGraphicsEffect(None)
        self.run_phase_5_word_reveal()

    # --- Phase 5: Word-by-Word Sentence Reveal (300ms/word) ---
    def run_phase_5_word_reveal(self):
        self.state = OverlayState.REVEALING_WORDS
        self.current_word_idx = 0
        self.msg_label.setText("")

        if not self.words:
            self.run_phase_6_active_state()
            return

        self.schedule_next_word()

    def schedule_next_word(self):
        if self.current_word_idx >= len(self.words):
            self.run_phase_6_active_state()
            return

        # Reveal words up to current_word_idx
        self.current_word_idx += 1
        current_text = " ".join(self.words[: self.current_word_idx])
        self.msg_label.setText(current_text)

        if self.current_word_idx < len(self.words):
            prev_word = self.words[self.current_word_idx - 1]
            # Extra pause on punctuation
            if re.search(r"[\.,!\?:;]$", prev_word):
                delay = PUNCTUATION_PAUSE_MS
            else:
                delay = WORD_INTERVAL_MS

            self.word_timer = QTimer(self)
            self.word_timer.setSingleShot(True)
            self.word_timer.timeout.connect(self.schedule_next_word)
            self.word_timer.start(delay)
        else:
            # All words revealed
            self._later(200, self.run_phase_6_active_state)

    # --- Phase 6: Active State & Countdown ---
    def run_phase_6_active_state(self):
        if self.state == OverlayState.ACTIVE and self._active_deadline is not None:
            return
        self.state = OverlayState.ACTIVE
        self.btn_widget.show()
        self.remaining_seconds = REMINDER_SECONDS
        self._active_deadline = time.monotonic() + REMINDER_SECONDS
        self.timer_label.setText(f"Auto-dismiss in {REMINDER_SECONDS}s")
        self.timer_label.show()
        self.countdown_timer = QTimer(self)
        self.countdown_timer.setTimerType(Qt.PreciseTimer)
        self.countdown_timer.setInterval(100)
        self.countdown_timer.timeout.connect(self.tick_countdown)
        self.countdown_timer.start()

    def tick_countdown(self):
        if self.state != OverlayState.ACTIVE or self._active_deadline is None:
            return
        self.remaining_seconds = max(0, math.ceil(self._active_deadline - time.monotonic()))
        self.timer_label.setText(f"Auto-dismiss in {self.remaining_seconds}s")
        if self.remaining_seconds == 0:
            self.countdown_timer.stop()
            self.request_close()

    def jump_to_active_state(self):
        """Instant final state for reduced motion, with the same 20-second timer."""
        self._web_progress = 1.0
        self.set_spidey_y_offset(self.spidey_target_y_offset)
        self.spidey_label.show()
        self.card.show()
        self.card.setGraphicsEffect(None)
        self.msg_label.setText(self.full_sentence)
        self.run_phase_6_active_state()

    def _later(self, milliseconds, callback):
        """Parent delayed steps to this window so closing cancels them."""
        timer = QTimer(self)
        timer.setSingleShot(True)
        self._pending_timers.append(timer)
        def fire():
            self._pending_timers.remove(timer)
            timer.deleteLater()
            callback()
        timer.timeout.connect(fire)
        timer.start(milliseconds)

    def _stop_activity(self):
        for timer in self.findChildren(QTimer):
            timer.stop()
        for animation in self.findChildren(QPropertyAnimation):
            animation.stop()

    def closeEvent(self, event):
        self._stop_activity()
        self.state = OverlayState.HIDDEN
        super().closeEvent(event)

    # --- User Actions & Exit Sequence ---
    def request_close(self):
        self.start_exit_sequence(self.on_done_cb)

    def request_snooze(self):
        self.start_exit_sequence(self.on_snooze_cb)

    def start_exit_sequence(self, callback: Callable[[], None]):
        """Cancellable exit sequence."""
        if self.state in (
            OverlayState.EXITING_CARD,
            OverlayState.ASCENDING,
            OverlayState.RETRACTING_WEB,
            OverlayState.HIDDEN,
        ):
            return  # Already exiting!

        self._stop_activity()

        self.exit_callback = callback

        if self.reduced_motion:
            self.finish_exit()
        else:
            self.run_exit_1_close_card()

    # --- Exit Step 1: Close Card (250ms) ---
    def run_exit_1_close_card(self):
        self.state = OverlayState.EXITING_CARD

        self.card_opacity = QGraphicsOpacityEffect(self.card)
        self.card.setGraphicsEffect(self.card_opacity)

        self.anim_exit_card = QPropertyAnimation(
            self.card_opacity, b"opacity", self
        )
        self.anim_exit_card.setDuration(EXIT_CARD_MS)
        self.anim_exit_card.setStartValue(1.0)
        self.anim_exit_card.setEndValue(0.0)
        self.anim_exit_card.setEasingCurve(QEasingCurve.InCubic)
        self.anim_exit_card.finished.connect(self.run_exit_2_ascend_spidey)
        self.anim_exit_card.start()

    # --- Exit Step 2: Spider-Man Ascends Web (700ms) ---
    def run_exit_2_ascend_spidey(self):
        self.state = OverlayState.ASCENDING
        self.card.hide()
        self.card.setGraphicsEffect(None)

        self.anim_ascend = QPropertyAnimation(self, b"spidey_y_offset", self)
        self.anim_ascend.setDuration(ASCEND_MS)
        self.anim_ascend.setStartValue(self._spidey_y_offset)
        self.anim_ascend.setEndValue(-self.spidey_height)
        self.anim_ascend.setEasingCurve(QEasingCurve.InCubic)
        self.anim_ascend.finished.connect(self.run_exit_3_retract_web)
        self.anim_ascend.start()

    # --- Exit Step 3: Retract Web Strand (350ms) ---
    def run_exit_3_retract_web(self):
        self.state = OverlayState.RETRACTING_WEB

        self.anim_retract = QPropertyAnimation(self, b"web_progress", self)
        self.anim_retract.setDuration(RETRACT_WEB_MS)
        self.anim_retract.setStartValue(1.0)
        self.anim_retract.setEndValue(0.0)
        self.anim_retract.setEasingCurve(QEasingCurve.InQuad)
        self.anim_retract.finished.connect(self.finish_exit)
        self.anim_retract.start()

    def finish_exit(self):
        self.state = OverlayState.HIDDEN
        self.close()
        callback = getattr(self, "exit_callback", None)
        self.exit_callback = None
        if callback:
            callback()
