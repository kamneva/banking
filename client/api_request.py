import requests
import json
from PySide6.QtCore import QDate

from gui.shared import date_format
from gui.currency_selector import Currency, currency_to_str

class APIRequest:
    base_url = "http://127.0.0.1:5000"

    def get(self, url, **kargs) -> dict | None:
        response = requests.get(url, **kargs)

        if response.status_code != 200:
            return None

        return json.loads(response.text)

    def post(self, url, **kargs) -> bool:
        return requests.post(url, **kargs).status_code == 200

    def get_config(self) -> dict | None:
        url = f"{APIRequest.base_url}/config"
        return self.get(url)

    def save_config(self, currency_list : list[Currency], time : list[str]) -> bool:
        url = f"{APIRequest.base_url}/config-update"
        params = {
            "currencies" : ",".join([currency_to_str(currency) for currency in currency_list]),
            "time" : ",".join(time)
        }
        return self.post(url, params=params)

    def update(self, start_date : QDate, end_date :QDate) -> bool:
        url = f"{APIRequest.base_url}/update"
        params = {
            "start_date" : start_date.toString(date_format),
            "end_date" : end_date.toString(date_format)
        }
        return self.post(url, params=params)

    def get_report(self, start_date : QDate, end_date : QDate, currency_list : list[Currency]) -> dict:
        url = f"{APIRequest.base_url}/report"
        params = {
            "start_date" : start_date.toString(date_format),
            "end_date" : end_date.toString(date_format),
            "currencies" : ",".join([currency_to_str(currency) for currency in currency_list])
        }
        return self.get(url, params=params)

request = APIRequest()