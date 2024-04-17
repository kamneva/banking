import json
from PySide6.QtWidgets import QWidget, QTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout

from gui.shared import general_font, header_font

from gui.currency_selector import CurrencySelector, str_to_currency
from gui.interval_widget import IntervalWidget
from gui.time_list import TimeList

from api_request import request

class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.interval_widget = IntervalWidget()
        self.currency_selector = CurrencySelector()
        self.time_list = TimeList()

        self.update_btn = QPushButton("Синхронизировать данные")
        self.update_btn.setFont(general_font)
        self.update_btn.clicked.connect(self.on_update_btn_clicked)

        self.report_btn = QPushButton("Отчёт")
        self.report_btn.setFont(general_font)
        self.report_btn.clicked.connect(self.on_report_btn_clicked)

        self.config_btn = QPushButton("Обновить конфигурацию")
        self.config_btn.setFont(general_font)
        self.config_btn.clicked.connect(self.on_config_btn_clicked)

        self.json_viewer = QTextEdit()
        self.json_viewer.setFont(header_font)
        self.json_viewer.setReadOnly(True)
        self.json_viewer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.control_layout = QHBoxLayout()
        self.control_layout.addStretch(0)
        self.control_layout.addWidget(self.update_btn)
        self.control_layout.addWidget(self.report_btn)
        self.control_layout.addWidget(self.config_btn)
        self.control_layout.addStretch(0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.interval_widget)
        self.main_layout.addWidget(self.currency_selector)
        self.main_layout.addWidget(self.time_list)
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addWidget(self.json_viewer)

        config = request.get_config()
        self.currency_selector.set_selected([str_to_currency(currency_str) for currency_str in config["currencies"]])
        self.time_list.set_time(config["time"])

    def on_update_btn_clicked(self) -> None:
        request.update(self.interval_widget.start_date(), self.interval_widget.end_date())

    def on_report_btn_clicked(self) -> None:
        currency_list = self.currency_selector.selected()
        start_date = self.interval_widget.start_date()
        end_date = self.interval_widget.end_date()

        report = request.get_report(start_date, end_date, currency_list)
        self.json_viewer.setText(json.dumps(report, indent=len(report.keys()), sort_keys=True))

    def on_config_btn_clicked(self) -> None:
        request.save_config(self.currency_selector.selected(), self.time_list.time())