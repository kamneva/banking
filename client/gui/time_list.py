from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout

from gui.shared import general_font, header_font

from gui.time_dialog import TimeDialog

class TimeList(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.caption_label = QLabel("Время обновления", alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.list_widget = QListWidget()
        self.list_widget.setFont(general_font)
        self.list_widget.addItems([ "Время1", "Время2" ])

        self.add_btn = QPushButton("Добавить")
        self.add_btn.setFont(general_font)
        self.add_btn.clicked.connect(self.on_add_btn_clicked)

        self.modify_btn = QPushButton("Изменить")
        self.modify_btn.setFont(general_font)
        self.modify_btn.clicked.connect(self.on_modify_btn_clicked)

        self.remove_btn = QPushButton("Удалить")
        self.remove_btn.setFont(general_font)
        self.remove_btn.clicked.connect(self.on_remove_btn_clicked)

        self.control_layout = QVBoxLayout()
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.control_layout.addWidget(self.add_btn)
        self.control_layout.addWidget(self.modify_btn)
        self.control_layout.addWidget(self.remove_btn)
        self.control_layout.addStretch(0)

        self.list_layout = QHBoxLayout()
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.addWidget(self.list_widget, 1)
        self.list_layout.addLayout(self.control_layout, 0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.caption_label)
        self.main_layout.addLayout(self.list_layout)

    def on_add_btn_clicked(self) -> None:
        dialog = TimeDialog()
        if not dialog.exec():
            return

        self.list_widget.addItem(dialog.time())
        self.list_widget.sortItems()

    def on_modify_btn_clicked(self) -> None:
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) == 0:
            return

        selected_item = selected_items[0]
        dialog = TimeDialog(selected_item.text())
        if not dialog.exec():
            return

        selected_item.setText(dialog.time())
        self.list_widget.sortItems()

    def on_remove_btn_clicked(self) -> None:
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) == 0:
            return

        item_row = self.list_widget.row(selected_items[0])
        self.list_widget.takeItem(item_row)

    def time(self) -> list[str]:
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count())]

    def set_time(self, time : list[str]) -> None:
        self.list_widget.clear()
        self.list_widget.addItems(time)
        self.list_widget.sortItems()