import os

from trading_strategies.coinbase_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_tools.coinbase_cmo_calculation import coinbase_cmo_logic_no_pandas
from trading_tools.coinbase_pro_wrapper.authenticated_client import AuthenticatedClient
from trading_tools.coinbase_pro_wrapper.public_client import PublicClient


def get_balance(coinbase_wrapper, ticker: str):
    '''
    Function to parse the get_accounts output to find the balance for a given ticker
    :param ticker: the ticker for the cryptocurrency that you want the balnace for e.g. BTC
    :return:
    '''

    all_accounts = coinbase_wrapper.get_accounts()

    response = None
    for account in all_accounts:
        if account['currency'] == ticker:
            response = account

    assert response is not None
    return response


def close_positions(coinbase_wrapper, pair, rate, amount):
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

    # base_currency = LOGICAL_PARAMS['PAIR'].split('-')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('-')[1]

    # if we have any of our quote_currency #TODO check the output for the .get_accounts() below
    if float(get_balance(coinbase_wrapper, ticker=quote_currency)['balance']) > 0 and LOGICAL_PARAMS["DRY_RUN"] is False:
        # sell the entire balance of our base currency
        response = coinbase_wrapper.sell(
            price=rate,
            size=amount,
            order_type='market',
            product_id=pair
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


def enter_position(coinbase_wrapper, pair, rate, amount):
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
        response = coinbase_wrapper.buy(price=rate,
                                        size=amount,
                                        order_type='market',
                                        product_id=pair)
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

    coinbase_wrapper = AuthenticatedClient(
        key=os.getenv('API_KEY'),
        b64secret=os.getenv('API_SECRET'),
        passphrase=os.getenv('PASSPHRASE'),
        api_url="https://api.pro.coinbase.com"
    )

    base_currency = LOGICAL_PARAMS['PAIR'].split('-')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('-')[1]
    assert base_currency+'-'+quote_currency == LOGICAL_PARAMS['PAIR']

    cmo = coinbase_cmo_logic_no_pandas(pair=LOGICAL_PARAMS['PAIR'], period=LOGICAL_PARAMS['PERIOD'])

    product_details = PublicClient().get_product_ticker(product_id='BTC-USD')
    rate = float(product_details['ask'])
    price = LOGICAL_PARAMS['INITIAL_CAPITAL'] * LOGICAL_PARAMS['ENTRY_SIZE']  # of base currency
    entry_amount = price/rate

    # asset oversold
    if cmo < LOGICAL_PARAMS["OVERSOLD_VALUE"]:
        response = enter_position(
            coinbase_wrapper,
            pair=LOGICAL_PARAMS['PAIR'],
            rate=rate,
            amount=entry_amount
        )
    # asset overbought
    elif cmo > LOGICAL_PARAMS["OVERBOUGHT_VALUE"]:
        response = close_positions(
            coinbase_wrapper,
            pair=LOGICAL_PARAMS['PAIR'],
            rate=rate,
            amount=entry_amount
        )
    else:
        response = 'no trades'

    print(f"{base_currency} balance: {get_balance(coinbase_wrapper, ticker=base_currency)['balance']}")
    print(f"{quote_currency} balance: {get_balance(coinbase_wrapper, ticker=quote_currency)['balance']}")

    print(f'CMO: {cmo}')
    print(f'response: {response}')
    for key in LOGICAL_PARAMS:
        print(f'{key}: {LOGICAL_PARAMS[key]}')


if __name__ == '__main__':
    lambda_handler(0, 0)
