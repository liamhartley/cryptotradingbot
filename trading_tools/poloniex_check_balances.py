import os
from trading_tools.poloniex_wrapper_bwentzloff import Poloniex

CRYPTO_PAIR = 'BTC_XRP'

if __name__ == '__main__':

    # TODO write a decorator that logs you in
    poloniex_wrapper = Poloniex(
        APIKey=os.getenv('POLONIEX_KEY'),
        Secret=os.getenv('POLONIEX_SECRET')
    )

    trade_history = poloniex_wrapper.returnMarketTradeHistory(currencyPair=CRYPTO_PAIR)
    print(trade_history)
