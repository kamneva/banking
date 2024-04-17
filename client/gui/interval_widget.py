from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QWidget, QLabel, QDateEdit, QVBoxLayout, QHBoxLayout

from gui.shared import general_font, header_font

class IntervalWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.caption_label = QLabel("Интервал обновления", alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.start_date_label = QLabel("С")
        self.start_date_label.setFont(general_font)

        self.start_date_edit = QDateEdit(QDate.currentDate())
        self.start_date_edit.setFont(general_font)

        self.end_date_label = QLabel("По")
        self.end_date_label.setFont(general_font)

        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit.setFont(general_font)

        self.interval_layout = QHBoxLayout()
        self.interval_layout.addStretch(0)
        self.interval_layout.addWidget(self.start_date_label)
        self.interval_layout.addWidget(self.start_date_edit)
        self.interval_layout.addStretch(0)
        self.interval_layout.addWidget(self.end_date_label)
        self.interval_layout.addWidget(self.end_date_edit)
        self.interval_layout.addStretch(0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.caption_label)
        self.main_layout.addLayout(self.interval_layout)

    def start_date(self) -> QDate:
        return self.start_date_edit.date()

    def end_date(self) -> QDate:
        return self.end_date_edit.date()