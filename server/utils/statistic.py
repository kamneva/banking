from models.currency import Currency

class Statistic:
    def get_min_value(currency_list : list[Currency], currency_code : str) -> float | None:
        if len(currency_list) == 0:
            return None

        min = currency_list[0].get(currency_code)
        for currency in currency_list:
            if currency.get(currency_code) < min:
                min = currency.get(currency_code)

        return min

    def get_max_value(currency_list : list[Currency], currency_code : str) -> float | None:
        if len(currency_list) == 0:
            return None

        max = currency_list[0].get(currency_code)
        for currency in currency_list:
            if currency.get(currency_code) > max:
                max = currency.get(currency_code)

        return max

    def get_avg_value(currency_list : list[Currency], currency_code : str) -> float | None:
        if len(currency_list) == 0:
            return None

        sum = 0
        for currency in currency_list:
            sum += currency.get(currency_code)

        return sum / len(currency_list)