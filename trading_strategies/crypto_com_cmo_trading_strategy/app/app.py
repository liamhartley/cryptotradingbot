import os

from trading_strategies.poloniex_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_tools.poloniex_cmo_calculation import poloniex_cmo_logic_no_pandas
from trading_tools.crypto_com_api_wrapper import CryptoComApi

def close_positions(poloniex_wrapper, pair, rate, amount):
    '''

    :param currency_pair: A string that defines the market, "USDT_BTC" for example.
    :param rate: The price. Units are market quote currency. Eg USDT_BTC market, the value of this field would be around 10,000. Naturally this will be dated quickly but should give the idea.
    :param amount: The total amount offered in this buy order.
    :return:
    '''
    print('closing position')
    print(f'entry_amount: {amount}')
    print(f'rate: {rate}')
    print(f'ticker: {pair}')

    # base_currency = LOGICAL_PARAMS['PAIR'].split('_')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('_')[1]

    # if we have any of our quote_currency
    if float(poloniex_wrapper.private_query(command='returnBalances')[quote_currency]) > 0 and LOGICAL_PARAMS["DRY_RUN"] is False:
        # sell the entire balance of our base currency
        response = poloniex_wrapper.trade(
            currency_pair=pair,
            rate=rate,
            amount=amount,
            command='sell'
        )
    elif LOGICAL_PARAMS["DRY_RUN"] is True:
        print(f"closing {LOGICAL_PARAMS['PAIR']}\nsale price: {pair['highestBid']}")
        response = {'orderNumber': '514845991795',
                    'resultingTrades': [
                        {'amount': '3.0',
                         'date': '2018-10-25 23:03:21',
                         'rate': '0.0002',
                         'total': '0.0006',
                         'tradeID': '251834',
                         'type': 'sell'}
                    ],
                    'fee': '0.01000000',
                    'clientOrderId': '12345',
                    'currencyPair': 'BTC_ETH'}
    else:
        response = None

    return response


def enter_position(poloniex_wrapper, pair, rate, amount):
    '''

    :param currency_pair: A string that defines the market, "USDT_BTC" for example.
    :param rate: The price. Units are market quote currency. Eg USDT_BTC market, the value of this field would be around 10,000. Naturally this will be dated quickly but should give the idea.
    :param amount: The total amount offered in this buy order.
    :return:
    '''
    print('entering position')
    print(f'entry_amount: {amount}')
    print(f'rate: {rate}')
    print(f'ticker: {pair}')

    if LOGICAL_PARAMS["DRY_RUN"] is False:
        response = poloniex_wrapper.trade(
            currency_pair=pair,
            rate=rate,
            amount=amount,
            command='buy'
        )
    else:
        print(f"opening: {LOGICAL_PARAMS['PAIR']}\nsize: {amount}\npurchase price: {pair['lowestAsk']} ")
        response = {'orderNumber': '514845991795',
                    'resultingTrades': [
                        {'amount': '3.0',
                         'date': '2018-10-25 23:03:21',
                         'rate': '0.0002',
                         'total': '0.0006',
                         'tradeID': '251834',
                         'type': 'buy'}
                    ],
                    'fee': '0.01000000',
                    'clientOrderId': '12345',
                    'currencyPair': 'BTC_ETH'}

    return response


def lambda_handler(event, context):

    crypto_wrapper = CryptoComApi() # TODO

    poloniex_wrapper = Poloniex(
        APIKey=os.getenv('POLONIEX_KEY'),
        Secret=os.getenv('POLONIEX_SECRET')
    )

    base_currency = LOGICAL_PARAMS['PAIR'].split('_')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('_')[1]
    assert base_currency+'_'+quote_currency == LOGICAL_PARAMS['PAIR']

    cmo = poloniex_cmo_logic_no_pandas()

    all_tickers = poloniex_wrapper.public_query(command='returnTicker')
    ticker = all_tickers[LOGICAL_PARAMS['PAIR']]
    rate = float(ticker['lowestAsk'])
    price = LOGICAL_PARAMS['INITIAL_CAPITAL'] * LOGICAL_PARAMS['ENTRY_SIZE']  # of base currency
    entry_amount = price/rate

    # asset oversold
    if cmo < LOGICAL_PARAMS["OVERSOLD_VALUE"]:
        response = enter_position(
            poloniex_wrapper,
            pair=LOGICAL_PARAMS['PAIR'],
            rate=rate,
            amount=entry_amount
        )
    # asset overbought
    elif cmo > LOGICAL_PARAMS["OVERBOUGHT_VALUE"]:
        response = close_positions(
            poloniex_wrapper,
            pair=LOGICAL_PARAMS['PAIR'],
            rate=rate,
            amount=entry_amount
        )
    else:
        response = 'no trades'

    print(f"{base_currency} balance: {poloniex_wrapper.private_query(command='returnBalances')[base_currency]}")
    print(f"{quote_currency} balance: {poloniex_wrapper.private_query(command='returnBalances')[quote_currency]}")

    print(f'CMO: {cmo}')
    print(f'response: {response}')
    for key in LOGICAL_PARAMS:
        print(f'{key}: {LOGICAL_PARAMS[key]}')


if __name__ == '__main__':
    lambda_handler(0, 0)
