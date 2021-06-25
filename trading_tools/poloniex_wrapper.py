import os
import time
import requests
import hashlib
import hmac
import urllib
import ssl
import json

from trading_strategies.poloniex_cmo_trading_strategy.config import LOGICAL_PARAMS


class Poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = bytes(Secret.encode('utf8'))
        self.public_url = 'https://poloniex.com/public?command='
        self.private_url = 'https://poloniex.com/tradingApi'

    def public_query(self, command):
        gcontext = ssl.SSLContext()
        data = urllib.request.urlopen(urllib.request.Request(self.public_url+command), context=gcontext)
        return json.loads(data.read())

    def private_query(self, command):
        payload = {
            'command': command,
            'nonce': int(time.time() * 1000),
        }

        paybytes = urllib.parse.urlencode(payload).encode('utf8')
        sign = hmac.new(self.Secret, paybytes, hashlib.sha512).hexdigest()

        headers = {
            'Key': self.APIKey,
            'Sign': sign
        }

        r = requests.post(self.private_url, headers=headers, data=payload)
        return r.json()

    def trade(self, currency_pair, rate, amount, command):
        '''

        :param currency_pair: A string that defines the market, "USDT_BTC" for example.
        :param rate: The price. Units are market quote currency. Eg USDT_BTC market, the value of this field would be around 10,000. Naturally this will be dated quickly but should give the idea.
        :param amount: The total amount offered in this buy order.
        :return:
        '''
        url = 'https://poloniex.com/tradingApi'
        payload = {
            'command': command,
            'nonce': int(time.time() * 1000),
            'currencyPair': currency_pair,
            'rate': rate,
            'amount': amount
        }
        paybytes = urllib.parse.urlencode(payload).encode('utf8')
        sign = hmac.new(self.Secret, paybytes, hashlib.sha512).hexdigest()

        headers = {
            'Key': self.APIKey,
            'Sign': sign
        }

        r = requests.post(url, headers=headers, data=payload)
        return r.json()


if __name__ == '__main__':

    # TODO write a decorator that logs you in - (still required??)
    poloniex_wrapper = Poloniex(
        APIKey=os.getenv('POLONIEX_KEY'),
        Secret=os.getenv('POLONIEX_SECRET')
    )

    all_tickers = poloniex_wrapper.public_query(command='returnTicker')
    ticker = all_tickers[LOGICAL_PARAMS['PAIR']]
    rate = float(ticker['lowestAsk'])
    price = LOGICAL_PARAMS['INITIAL_CAPITAL'] * LOGICAL_PARAMS['ENTRY_SIZE']  # of base currency
    entry_amount = price/rate

    # response = poloniex_wrapper.trade(
    #     currency_pair=LOGICAL_PARAMS['PAIR'],
    #     rate=rate,
    #     amount=entry_amount,
    #     command='buy'
    # )

    response = poloniex_wrapper.trade(
        currency_pair=LOGICAL_PARAMS['PAIR'],
        rate=rate,
        amount=entry_amount,
        command='sell'
    )

    balance = poloniex_wrapper.private_query(command='returnBalances')

    print(balance)
