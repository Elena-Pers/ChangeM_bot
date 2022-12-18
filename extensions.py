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
            raise APIException (f"Валюта {base} не найдена")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException (f"Валюта {quote} не найдена")

        if base_key == quote_key:
            raise APIException (f"Невозможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException (f'Не удалось обработать количество {amount}')

        if amount <= 0:
            raise APIException(f'Введите количество больше 0')


        payload = {}
        headers = {"apikey": "RcVVAWN2cuevj3Xpdxlce8Bbm2y69Hh1"}
        response = requests.request("GET", f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={quote_key}&amount={amount}", headers=headers, data=payload)
        resp = json.loads(response.content)
        return resp["result"]
