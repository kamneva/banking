class CurrencyCode:
    eur = "EUR"
    rub = "RUB"
    usd = "USD"

    def all() -> list[str]:
        return [ 
            CurrencyCode.eur,
            CurrencyCode.rub,
            CurrencyCode.usd
        ]