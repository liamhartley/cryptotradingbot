#!/usr/bin/python
# coding: utf8

# Full credit goes to Igor Jakovljevic for the code located here https://github.com/IgorJakovljevic/crypto-com-api

import requests
import hashlib
import datetime


class CryptoComApi():
    def __init__(self, time_offset=0, api_key="", secret_key=""):
        self.url = "https://api.crypto.com"
        self.api_key = api_key
        self.secret_key = secret_key
        self.time_offset = time_offset

    def get_symbols(self):
        """ Queries all transaction pairs and precision supported by the system
        Returns:
            [list] -- list of all transaction pairs and precision supported by the system
        """

        return requests.get(self.url + "/v1/symbols").json()['data']

    def get_ticker(self, symbol):
        """ Gets the current market quotes
        Arguments:
            symbol {string} -- Market mark e.g. btcusdt
        Returns:
            [dict] -- Returns current market quotes of the given symbol.
        """

        request_url = f"{self.url}/v1/ticker?symbol={symbol}"
        return requests.get(request_url).json()['data']

    def get_trades(self, symbol):
        """ Obtains market transaction records.
        Arguments:
            symbol {string} -- Market mark e.g. btcusdt
        Returns:
            [list] -- Returns a list of market transaction records
        """
        request_url = f"{self.url}/v1/trades?symbol={symbol}"
        return requests.get(request_url).json()['data']

    def get_market_trades(self):
        """ Gets the latest transaction price of each pair of currencies
        Arguments:
            symbol {string} -- Market mark e.g. btcusdt
        Returns:
            [list] -- List of latest transaction price of each pair of currencies
        """
        request_url = f"{self.url}/v1/ticker/price"
        return requests.get(request_url).json()['data']

    def get_orders(self, symbol, step="step1"):
        """ Gets the list of orders from buyers and sellers for the market
        Arguments:
            symbol {[string]} -- Market mark, ethbtc, See below for details
        Keyword Arguments:
            step {str} -- The depth type -- options: step0, step1, step2 (Merger depth0-2).
                step0time is the highest accuracy (default: {"step1"})
        Returns:
            [list] -- List of orders from buyers and sellers for the market
        """
        request_url = f"{self.url}/v1/depth?symbol={symbol}&type={step}"
        return requests.get(request_url).json()['data']

    def get_k_lines(self, symbol, period, format_data=False):
        """ Gets K-line data for symbol for a given period
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
            period {int} -- Given in minutes. Possible values are [1, 5, 15, 30, 60, 1440, 10080, 43200]
                    which corresponds to 1min, 5min, 15min, 30min, 1hour, 1day, 1week, 1month.
        Keyword Arguments:
            format_data {bool} -- If set to true the output elements are formated as a dictionary (default: {False})
        Returns:
            [list] -- Returns K-line data for symbol for a given period
        """
        request_url = f"{self.url}/v1/klines?symbol={symbol}&period={period}"
        data = requests.get(request_url).json()['data']
        if (not format_data):
            return data

        def parse_obj(val):
            ret = dict()
            ret["ts"] = val[0]
            ret["open"] = val[1]
            ret["high"] = val[2]
            ret["min"] = val[3]
            ret["close"] = val[4]
            ret["volume"] = val[5]
            return ret

        return [parse_obj(x) for x in data]

    def sign(self, params: dict):
        sign_str = ""
        # sort params alphabetically and add to signing string
        for param in sorted(params.keys()):
            sign_str += param + str(params[param])
        # at the end add the secret
        sign_str += str(self.secret_key)
        hash = hashlib.sha256(sign_str.encode()).hexdigest()
        return hash

    def mandatory_post_params(self):
        data = dict()
        data['api_key'] = self.api_key
        data['time'] = int(datetime.datetime.now().timestamp() * 1000) - int(self.time_offset)
        return data

    def get_account(self):
        data = self.mandatory_post_params()
        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/account"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def get_all_orders(self, symbol, page=None, pageSize=None, startDate=None, endDate=None):
        """ Gets all orders of the user
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
        Keyword Arguments:
            page {int} -- Page number
            pageSize {int} -- pageSize
            startDate {string} -- Start time, accurate to seconds "yyyy-MM-dd mm:hh:ss"
            endDate {string} -- End time, accurate to seconds "yyyy-MM-dd mm:hh:ss"
        Returns:
            {'count': int, 'resultList': list} -- Returns object with a result list and number of elements
        """
        data = self.mandatory_post_params()
        data['symbol'] = symbol

        if (page is not None):
            data['page'] = page
        if (pageSize is not None):
            data['pageSize'] = pageSize
        if (startDate is not None):
            data['startDate'] = startDate
        if (endDate is not None):
            data['endDate'] = endDate

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/allOrders"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def get_open_orders(self, symbol, page=None, pageSize=None):
        """ Gets all open orders of the user
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
        Keyword Arguments:
            page {int} -- Page number
            pageSize {int} -- pageSize
        Returns:
            {'count': int, 'resultList': list} -- Returns object with a result list and number of elements
        """

        data = self.mandatory_post_params()
        data['symbol'] = symbol

        if (page is not None):
            data['page'] = page
        if (pageSize is not None):
            data['pageSize'] = pageSize

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/openOrders"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def get_trades(self, symbol, page=None, pageSize=None, startDate=None, endDate=None, sort=None):
        """ Gets all trades of the user
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
        Keyword Arguments:
            page {int} -- Page number
            pageSize {int} -- pageSize
            startDate {string} -- Start time, accurate to seconds "yyyy-MM-dd mm:hh:ss"
            endDate {string} -- End time, accurate to seconds "yyyy-MM-dd mm:hh:ss"
            sort {int} -- 1 gives reverse order
        Returns:
            {'count': int, 'resultList': list} -- Returns object with a result list and number of elements
        """

        data = self.mandatory_post_params()
        data['symbol'] = symbol

        if (page is not None):
            data['page'] = page
        if (pageSize is not None):
            data['pageSize'] = pageSize
        if (startDate is not None):
            data['startDate'] = startDate
        if (endDate is not None):
            data['endDate'] = endDate
        if (sort is not None):
            data['sort'] = sort

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/openOrders"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def get_order(self, symbol, order_id):
        """ Gets specific order of the user
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
            order_id {string} -- Id of the bid, not the order
        Returns:
            object -- Contains data about the whole order
        """

        data = self.mandatory_post_params()
        data['symbol'] = symbol
        data['order_id'] = order_id

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/showOrder"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def cancel_order(self, symbol, order_id):
        """ Cancels specific order of the user
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
            order_id {string} -- Id of the bid, not the order
        Returns:
            object -- Contains data about the whole order
        """

        data = self.mandatory_post_params()
        data['symbol'] = symbol
        data['order_id'] = order_id

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/orders/cancel"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def cancel_all_orders(self, symbol):
        """ Cancels specific order of the user
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
            order_id {string} -- Id of the bid, not the order
        Returns:
            object -- Contains data about the whole order
        """

        data = self.mandatory_post_params()
        data['symbol'] = symbol

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/cancelAllOrders"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(request_url, data=data, headers=headers).json()['data']

    def order(self, symbol, side, order_type=1, volume=0, price=None, fee_is_user_exchange_coin=1):
        """ Create a new order
        Arguments:
            symbol {string} -- Market mark e.g. bchbtc
            side {string} -- BUY, SELL
            type {int} -- Type of list: 1 for limit order (user sets a price), 2 for market order (best available price)
            volume {float} -- Purchase quantity (Polysemy, multiplexing fields) type=1 represents the quantity of sales and purchases type=2: buy means the total price, Selling represents the total number. Trading restrictions user/me-User information.

        Keyword Arguments:
            fee_is_user_exchange_coin {int} -- this parameter indicates whether to use the platform currency to pay the handling fee, 0 means no, 1 means yes. 0 when the exchange has the platform currency.
            price {float} -- Authorized unit price. If type=2 then no need for this parameter.
        Returns:
            object -- Contains data about the whole order
        """

        data = self.mandatory_post_params()

        if (price is not None):
            data['price'] = price
        else:
            return None

        data['symbol'] = symbol
        data['volume'] = volume
        data['type'] = order_type
        data['side'] = side

        if (fee_is_user_exchange_coin is not None):
            data['fee_is_user_exchange_coin'] = fee_is_user_exchange_coin

        data['sign'] = self.sign(data)

        request_url = f"{self.url}/v1/order"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        result = requests.post(request_url, data=data, headers=headers).json()
        return result['data']
