from datetime import datetime
from flask import Flask, jsonify, request
from sqlalchemy import and_

from models.currency import db, Currency

from utils.config import Config, app_config
from utils.currency_code import CurrencyCode
from utils.currency_request import CurrencyRequest
from utils.datetime_format import date_format
from utils.statistic import Statistic
from utils.synchronizer import Synchronizer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:7151@localhost:5432/banking"

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/update", methods=["POST"])
def update():
    currency_list = []
    if "start_date" in request.args.keys() and "end_date" in request.args.keys():
        start_date = datetime.strptime(request.args["start_date"], date_format)
        end_date = datetime.strptime(request.args["end_date"], date_format)

        currency_list = CurrencyRequest.get_currency_list_by_interval(start_date, end_date)
    else:
        currency = CurrencyRequest.get_currency_by_day(datetime.now())

        if currency is not None:
            currency_list.append(currency)

    for currency in currency_list:
        query = Currency.query.filter_by(date = currency.date).first()

        db.session.add(currency) if query is None else query.update(currency)
        db.session.commit()

    return jsonify()

@app.route("/report", methods=["GET"])
def report():
    json = {}

    start_date = datetime.strptime(request.args["start_date"], date_format).date()
    end_date = datetime.strptime(request.args["end_date"], date_format).date()

    for arg in request.args[Config.currencies_param_name].split(","):
        if arg not in CurrencyCode.all():
            continue

        column_name = arg.lower()
        query = Currency.query.filter(
            and_(
                Currency.__table__.columns[column_name].is_not(None),
                Currency.date >= start_date,
                Currency.date <= end_date
            )
        ).all()

        if len(query) == 0:
            json[arg] = None
            continue

        statistic = {
            "min" : Statistic.get_min_value(query, arg),
            "max" : Statistic.get_max_value(query, arg),
            "avg" : Statistic.get_avg_value(query, arg)
        }

        json[arg] = statistic

    return json

@app.route("/config", methods=["GET"])
def config():
    return app_config.json()

@app.route("/config-update", methods=["POST"])
def config_update():
    for arg in request.args:
        if arg == Config.currencies_param_name:
            app_config.set_currencies(request.args[Config.currencies_param_name].split(","))
        if arg == Config.time_param_name:
            app_config.set_time(request.args[Config.time_param_name].split(","))

    app_config.save()
    synchronizer.update()

    return jsonify()

if __name__ == "__main__":
    synchronizer = Synchronizer()
    synchronizer.start()

    app.run()

    synchronizer.stop()