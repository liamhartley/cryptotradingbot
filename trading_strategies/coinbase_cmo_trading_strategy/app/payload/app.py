import os

from trading_strategies.coinbase_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_tools.coinbase_pro_wrapper.authenticated_client import AuthenticatedClient
from trading_tools.coinbase_pro_wrapper.public_client import PublicClient
# from trading_tools.coinbase_cmo_calculation import coinbase_cmo_logic_no_pandas
from trading_tools.poloniex_cmo_calculation import poloniex_cmo_logic_no_pandas


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

    :param currency_pair: A string that defines the market, "ETH-USDC" for example.
    :param rate: The price. Units are market quote currency. Eg ETH-USDC market, the value of this field would be around 10,000. Naturally this will be dated quickly but should give the idea.
    :param amount: The total amount offered in this buy order.
    :return:
    '''
    print('----- closing position -----')
    print(f'entry_amount: {amount}')
    print(f'rate: {rate}')
    print(f'ticker: {pair}')

    # base_currency = LOGICAL_PARAMS['PAIR'].split('-')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('-')[1]

    # if we have any of our quote_currency
    if float(get_balance(coinbase_wrapper, ticker=quote_currency)['balance']) > 0 and LOGICAL_PARAMS["DRY_RUN"] is False:
        response = coinbase_wrapper.sell(
            # price=rate, not required for a market order
            size=round(amount, 8),
            order_type='market',
            product_id=pair
        )
    elif LOGICAL_PARAMS["DRY_RUN"] is True:
        print(f"closing {LOGICAL_PARAMS['PAIR']}\nsale price: {rate}")
        response = {'id': '0f27c0ce-5705-43e6-972a-c611ace696be', 'size': '0.00265321', 'product_id': 'ETH-USDC',
                    'side': 'sell', 'stp': 'dc', 'type': 'market', 'post_only': False,
                    'created_at': '2021-12-23T13:54:24.581751Z', 'fill_fees': '0', 'filled_size': '0',
                    'executed_value': '0', 'status': 'pending', 'settled': False}
    else:
        response = None

    return response


def enter_position(coinbase_wrapper, pair, rate, amount):
    '''

    :param currency_pair: A string that defines the market, "ETH-USDC" for example.
    :param rate: The price. Units are market quote currency. Eg ETH-USDC market, the value of this field would be around 10,000. Naturally this will be dated quickly but should give the idea.
    :param amount: The total amount offered in this buy order.
    :return:
    '''
    print('----- entering position -----')
    print(f'entry_amount: {amount}')
    print(f'rate: {rate}')
    print(f'ticker: {pair}')

    if LOGICAL_PARAMS["DRY_RUN"] is False:
        response = coinbase_wrapper.buy(# price=str(rate), not required for a market order
                                        size=str(round(amount, 8)),
                                        order_type='market',
                                        product_id=pair)
    else:
        print(f"opening: {LOGICAL_PARAMS['PAIR']}\nsize: {amount}\npurchase price: {rate} ")
        response = {'id': 'a118497f-702e-4d11-a8d4-443e50a94d8d', 'size': '0.00265487', 'product_id': 'ETH-USDC', 'side': 'buy',
                    'stp': 'dc', 'funds': '105.45273631', 'type': 'market', 'post_only': False,
                    'created_at': '2021-12-23T13:44:40.753983Z', 'fill_fees': '0', 'filled_size': '0', 'executed_value': '0',
                    'status': 'pending', 'settled': False}

    return response


def lambda_handler(event, context):

    coinbase_wrapper = AuthenticatedClient(
        key=os.getenv('COINBASE_API_KEY'),
        b64secret=os.getenv('COINBASE_API_SECRET'),
        passphrase=os.getenv('COINBASE_PASSPHRASE'),
        api_url="https://api.pro.coinbase.com"
    )

    base_currency = LOGICAL_PARAMS['PAIR'].split('-')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('-')[1]
    assert base_currency+'-'+quote_currency == LOGICAL_PARAMS['PAIR']

    cmo = poloniex_cmo_logic_no_pandas(pair=quote_currency+'_'+base_currency)

    product_details = PublicClient().get_product_ticker(product_id=LOGICAL_PARAMS['PAIR'])
    ask_price = float(product_details['ask'])
    trade_size = LOGICAL_PARAMS['INITIAL_CAPITAL'] * LOGICAL_PARAMS['ENTRY_SIZE']  # of base currency
    exit_amount = trade_size/ask_price
    # asset oversold
    if cmo < LOGICAL_PARAMS["OVERSOLD_VALUE"]:
        response = enter_position(
            coinbase_wrapper,
            pair=LOGICAL_PARAMS['PAIR'],
            rate=ask_price,
            amount=trade_size
        )
    # asset overbought
    elif cmo > LOGICAL_PARAMS["OVERBOUGHT_VALUE"]:
        response = close_positions(
            coinbase_wrapper,
            pair=LOGICAL_PARAMS['PAIR'],
            rate=ask_price,
            amount=exit_amount
        )
    else:
        response = 'no trades'

    print(f"{base_currency} balance: {get_balance(coinbase_wrapper, ticker=base_currency)['balance']}")
    print(f"{quote_currency} balance: {get_balance(coinbase_wrapper, ticker=quote_currency)['balance']}")

    print(f'CMO: {cmo}')
    print(f'response: {response}')
    print('Logical parameters:')
    for key in LOGICAL_PARAMS:
        print(f'{key}: {LOGICAL_PARAMS[key]}')


if __name__ == '__main__':
    lambda_handler(0, 0)
