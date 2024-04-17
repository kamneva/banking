import os
from configparser import ConfigParser, SectionProxy

from utils.currency_code import CurrencyCode
from utils.datetime_format import time_format

class Config:
    filename = "server.ini"
    section_name = "DEFAULT"
    currencies_param_name = "currencies"
    time_param_name = "time"

    def __init__(self) -> None:
        self.config = ConfigParser()

    def load(self) -> None:
        self.config.read(Config.filename)

    def save(self) -> None:
        with open(Config.filename, "w") as config_file:
            self.config.write(config_file)

    def section(self) -> SectionProxy:
        return self.config[Config.section_name]

    def currencies(self) -> list[str]:
        return self.section()[Config.currencies_param_name].split(",")

    def set_currencies(self, currencies : list[str]) -> None:
        self.section()[Config.currencies_param_name] = ",".join(currencies)

    def time(self) -> list[str]:
        return self.section()[Config.time_param_name].split(",")

    def set_time(self, time : list[str]):
        self.section()[Config.time_param_name] = ",".join(time)

    def json(self) -> dict:
        return {
            Config.currencies_param_name : self.currencies(),
            Config.time_param_name : self.time()
        }

app_config = Config()
if os.path.exists(Config.filename):
    app_config.load()
else:
    app_config.set_currencies([ CurrencyCode.cad, CurrencyCode.eur, CurrencyCode.usd ])
    app_config.set_time([ "00:00", "12:00" ])
app_config.save()