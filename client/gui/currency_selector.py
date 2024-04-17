from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QGridLayout

from enum import IntEnum

from gui.shared import general_font, header_font

class Currency(IntEnum):
        EUR = 0,
        RUB = 1,
        USD = 2

def currency_to_str(currency : Currency) -> str:
    match currency:
        case Currency.EUR:
            return "EUR"

        case Currency.RUB:
            return "RUB"

        case Currency.USD:
            return "USD"

    return ""

def str_to_currency(currency : str) -> Currency | None:
    if currency == "EUR":
        return Currency.EUR

    if currency == "RUB":
        return Currency.RUB

    if currency == "USD":
        return Currency.USD

    return None

class CurrencySelector(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.caption_label = QLabel("Валюты", alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.check_box_map = {
            Currency.EUR : QCheckBox(currency_to_str(Currency.EUR)),
            Currency.RUB : QCheckBox(currency_to_str(Currency.RUB)),
            Currency.USD : QCheckBox(currency_to_str(Currency.USD))
        }

        self.main_layout = QGridLayout(self)
        self.main_layout.addWidget(self.caption_label, 0, 0, 1, 3)
        for currency in self.check_box_map:
            check_box = self.check_box_map[currency]
            check_box.setFont(general_font)

            self.main_layout.addWidget(check_box, 1, int(currency))

    def selected(self) -> list[Currency]:
        selected_list = []
        for currency in self.check_box_map:
            if self.check_box_map[currency].isChecked():
                selected_list.append(currency)

        return selected_list

    def set_selected(self, selected : list[Currency]) -> None:
        for currency in self.check_box_map:
            self.check_box_map[currency].setChecked(selected.count(currency) != 0)