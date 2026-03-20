import os
import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from packages.core.db import fetch_unshown_user_alert, mark_user_alert_shown
from packages.audio_i18n.settings import load_settings, save_settings
from packages.audio_i18n.i18n import build_popup_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DISMISS_FILE = os.path.join(BASE_DIR, "dismiss.flag")


class DefenderUI(QWidget):
    def __init__(self):
        super().__init__()

        self.current_alert = None
        self.is_animating = False
        self.current_avatar_state = False

        assets_dir = os.path.join(BASE_DIR, "assets")
        self.flag_path = os.path.join(BASE_DIR, "speaking.flag")

        self.neutral_path = os.path.join(assets_dir, "avatar_neutral.png")
        self.talk_path = os.path.join(assets_dir, "avatar_talk.png")

        self.settings_obj = load_settings()

        self.setWindowTitle("Defender Companion")
        self.setFixedSize(760, 640)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.title_label = QLabel("🛡️ Defender Companion Alert")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "font-size: 26px; font-weight: bold; color: #d32f2f; margin: 10px;"
        )

        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.set_avatar(self.neutral_path)

        self.severity_label = QLabel("Severity: -")
        self.severity_label.setAlignment(Qt.AlignCenter)
        self.severity_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin: 6px;"
        )

        self.info_box = QTextEdit()
        self.info_box.setReadOnly(True)
        self.info_box.setStyleSheet("font-size: 14px; padding: 8px;")
        self.info_box.setMinimumHeight(320)

        self.lang_label = QLabel("Voice Language:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Hindi", "hi")
        self.lang_combo.addItem("Marathi", "mr")

        self.mute_checkbox = QCheckBox("Mute Voice")

        self.close_btn = QPushButton("I Understand")
        self.close_btn.setFixedWidth(160)
        self.close_btn.clicked.connect(self.hide_alert)

        self.load_ui_settings()

        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        self.mute_checkbox.stateChanged.connect(self.on_mute_changed)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.lang_label)
        controls_layout.addWidget(self.lang_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(self.mute_checkbox)
        controls_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.severity_label)
        layout.addLayout(controls_layout)
        layout.addWidget(self.info_box)
        layout.addWidget(self.close_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        self.hide()

        self.db_timer = QTimer()
        self.db_timer.timeout.connect(self.poll_db)
        self.db_timer.start(1000)

        self.speaking_timer = QTimer()
        self.speaking_timer.timeout.connect(self.check_speaking_status)
        self.speaking_timer.start(150)

        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate_avatar)
        self.anim_timer.setInterval(120)

    def load_ui_settings(self):
        lang = self.settings_obj.language

        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == lang:
                self.lang_combo.setCurrentIndex(i)
                break

        self.mute_checkbox.setChecked(not self.settings_obj.enabled)

    def on_language_changed(self):
        self.settings_obj.language = self.lang_combo.currentData()
        save_settings(self.settings_obj)
        self.refresh_current_alert_text()
        print(f"[UI] Language changed to {self.settings_obj.language}")

    def on_mute_changed(self):
        self.settings_obj.enabled = not self.mute_checkbox.isChecked()
        save_settings(self.settings_obj)
        print(f"[UI] Voice enabled: {self.settings_obj.enabled}")

    def set_avatar(self, image_path: str):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.avatar_label.setPixmap(scaled)
        else:
            self.avatar_label.setText("[Avatar missing]")

    def poll_db(self):
        try:
            alert = fetch_unshown_user_alert()
            if alert:
                self.display_alert(alert)
                mark_user_alert_shown(alert.id)
        except Exception as e:
            print(f"[UI ERROR] {e}")

    def display_alert(self, alert):
        self.current_alert = alert
        self.severity_label.setText(f"Severity: {alert.severity}")
        self.refresh_current_alert_text()

        self.show()
        self.raise_()
        self.activateWindow()

    def refresh_current_alert_text(self):
        if not self.current_alert:
            return

        lang = self.settings_obj.language
        content = build_popup_text(self.current_alert, lang)
        self.info_box.setPlainText(content)

    def hide_alert(self):
        try:
            with open(DISMISS_FILE, "w", encoding="utf-8") as f:
                f.write("dismissed")
        except Exception as e:
            print(f"[UI DISMISS ERROR] {e}")

        self.stop_lip_sync()
        self.hide()

    def start_lip_sync(self):
        if not self.is_animating:
            self.is_animating = True
            self.anim_timer.start()

    def stop_lip_sync(self):
        self.is_animating = False
        self.anim_timer.stop()
        self.set_avatar(self.neutral_path)

    def animate_avatar(self):
        if not self.is_animating:
            return

        if self.current_avatar_state:
            self.set_avatar(self.neutral_path)
        else:
            self.set_avatar(self.talk_path)

        self.current_avatar_state = not self.current_avatar_state

    def check_speaking_status(self):
        if os.path.exists(self.flag_path):
            self.start_lip_sync()
        else:
            self.stop_lip_sync()


def main():
    app = QApplication(sys.argv)
    window = DefenderUI()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()