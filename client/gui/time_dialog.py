from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import QDialog, QWidget, QLabel, QTimeEdit, QPushButton, QVBoxLayout, QHBoxLayout

from gui.shared import header_font, general_font, time_format

class TimeDialog(QDialog):
    def __init__(self, time : str = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.caption_label = QLabel("Задайте время", alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.time_edit = QTimeEdit(QTime.fromString(time, time_format) if time is not None else QTime())
        self.time_edit.setFont(general_font)

        self.ok_btn = QPushButton("ОК")
        self.ok_btn.setFont(general_font)
        self.ok_btn.clicked.connect(self.accept)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFont(general_font)
        self.cancel_btn.clicked.connect(self.reject)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addStretch(0)
        self.btn_layout.addWidget(self.ok_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.btn_layout.addStretch(0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.caption_label)
        self.main_layout.addWidget(self.time_edit)
        self.main_layout.addLayout(self.btn_layout)

    def time(self) -> str:
        return self.time_edit.time().toString(time_format)