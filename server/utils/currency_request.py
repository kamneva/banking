import re
import requests
from datetime import datetime

from utils.config import app_config
from utils.datetime_format import date_format

from models.currency import Currency

class CurrencyRequest:
    day_url = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt"
    year_url = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/year.txt"

    def get_currency_by_day(date : datetime) -> Currency | None:
        params = { "date" : date.strftime(date_format) }
        response = requests.get(CurrencyRequest.day_url, params=params)

        if response.status_code != 200:
            return None

        # TODO: Add config support
        currency_args = params

        content = response.content.decode()
        for line in content.split("\n"):
            if line.find("Country") != -1 or len(line) == 0:
                continue

            fields = line.split("|")
            if len(fields) != 5:
                fields[0] = re.sub(r" #[0-9]*", "", fields[0])
                data_date = datetime.strptime(fields[0], "%d %b %Y")

                if date.date() != data_date.date():
                    return None

                continue

            amount, currency_code, rate = fields[2], fields[3], fields[4]

            if currency_code not in app_config.currencies():
                continue

            currency_args[currency_code] = float(rate) / float(amount)

        return Currency(currency_args)

    def get_currency_list_by_interval(start_date : datetime, end_date : datetime) -> list[Currency]:
        currency_list = []

        for year in range(start_date.year, end_date.year + 1):
            params = { "year" : year }
            response = requests.get(CurrencyRequest.year_url, params=params)

            if response.status_code != 200:
                continue

            currency_index = {}
            currency_amount = {}

            content = response.content.decode()
            for line in content.split("\n"):
                currency_args = {}

                fields = line.split("|")
                if len(fields) < 2:
                    continue

                if line.find("Date") != -1:
                    for i in range(len(fields)):
                        if i == 0:
                            continue

                        currency_code = fields[i].split(" ")[1]
                        currency_index[currency_code] = i
                        currency_amount[currency_code] = float(fields[i].split(" ")[0])

                    continue

                date = datetime.strptime(fields[0], date_format)
                if date < start_date or date > end_date:
                    continue

                currency_args["date"] = fields[0]

                for currency_code in app_config.currencies():
                    if currency_index.get(currency_code) is None:
                        continue

                    currency_args[currency_code] = float(fields[currency_index[currency_code]]) / currency_amount[currency_code]

                currency_list.append(Currency(currency_args))

        return currency_list