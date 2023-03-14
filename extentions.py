import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            return APIException(f'Валюта {base} не найдена!')
        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            return APIException(f'Валюта {quote} не найдена!')

        if base_key == quote_key:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}!')

        try:
            amount = float(amount)
            if float(amount) > 1000000.000 or float(amount) < 0.001:
                raise APIException(f'Не удалось обработать указанное количество {amount}!')
        except ValueError:
            raise APIException(f'Не удалось обработать указанное количество {amount}!')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/0209dab98ae5fb9ba1be3293/pair/{base_key}/{quote_key}')
        cur_rate = json.loads(r.content)
        new_price = cur_rate['conversion_rate'] * amount
        new_price = round(new_price, 3)
        return new_price
