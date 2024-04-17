from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from utils.currency_code import CurrencyCode
from utils.datetime_format import date_format

db = SQLAlchemy()

class Currency(db.Model):
    __tablename__ = "currencies"

    date = db.Column(db.Date(), nullable = False, unique = True, primary_key = True)

    eur = db.Column(db.Float(), nullable = True)
    rub = db.Column(db.Float(), nullable = True)
    usd = db.Column(db.Float(), nullable = True)

    def __init__(self, args : dict) -> None:
        self.date = datetime.strptime(args.get("date"), date_format)

        self.eur = args.get(CurrencyCode.eur)
        self.rub = args.get(CurrencyCode.rub)
        self.usd = args.get(CurrencyCode.usd)

    def json(self) -> dict:
        return {
            "date" : self.date.strftime(date_format),
            CurrencyCode.eur : self.eur,
            CurrencyCode.rub : self.rub,
            CurrencyCode.usd : self.usd
        }

    def update(self, other) -> None:
        if other.eur is not None:
            self.eur = other.eur

        if other.rub is not None:
            self.rub = other.rub

        if other.usd is not None:
            self.usd = other.usd

    def get(self, currency_code) -> float | None:
        if currency_code == CurrencyCode.eur:
            return self.eur

        if currency_code == CurrencyCode.rub:
            return self.rub

        if currency_code == CurrencyCode.usd:
            return self.usd

        return None