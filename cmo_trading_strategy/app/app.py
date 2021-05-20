import os
import boto3

from gemini.helpers import poloniex
from cmo_trading_strategy.backtesting.backtesting import cmo_logic
from cmo_trading_strategy.config import LOGICAL_PARAMS, INFRASTRUCTURE_PARAMS
from trading_tools.poloniex_wrapper_bwentzloff import Poloniex


def check_cmo():
    past_data = poloniex.load_dataframe(
        pair=LOGICAL_PARAMS["PAIR"],
        period=LOGICAL_PARAMS["PERIOD"],
        days_history=LOGICAL_PARAMS["CMO_PERIOD"]
    )

    if len(past_data)-1 == LOGICAL_PARAMS["CMO_PERIOD"]:
        past_data = past_data[1:]
    elif len(past_data) == LOGICAL_PARAMS["CMO_PERIOD"]:
        pass
    else:
        raise Exception("Invalid CMO check")
    cmo = cmo_logic(past_data)
    return cmo


def close_positions(poloniex_wrapper, base_currency, quote_currency):

    ticker = poloniex_wrapper.returnTicker()[quote_currency+'_'+base_currency]

    # if we have any of our base currency
    if poloniex_wrapper.returnBalances()[base_currency] > 0 and LOGICAL_PARAMS["DRY_RUN"] is False:
        # sell the entire balance of our base currency
        response = poloniex_wrapper.sell(
            currencyPair=LOGICAL_PARAMS['PAIR'],
            rate=ticker['highestBid'],
            amount=poloniex_wrapper.returnBalances()[base_currency]
        )
    elif LOGICAL_PARAMS["DRY_RUN"] is True:
        print(f"closing {LOGICAL_PARAMS['PAIR']}\nsale price: {ticker['highestBid']}")
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

    print(f"{base_currency} balance: {poloniex_wrapper.returnBalances()[base_currency]}")
    return response


def enter_position(poloniex_wrapper, base_currency, quote_currency):
    ticker = poloniex_wrapper.returnTicker()[quote_currency+'_'+base_currency]
    entry_amount = ticker['lowestAsk']/(LOGICAL_PARAMS['INITIAL_CAPITAL'] * LOGICAL_PARAMS['ENTRY_SIZE'])
    if LOGICAL_PARAMS["DRY_RUN"] is False:
        response = poloniex_wrapper.buy(
            currencyPair=LOGICAL_PARAMS['PAIR'],
            rate=ticker['lowestAsk'],
            amount=entry_amount
        )
    else:
        print(f"opening: {LOGICAL_PARAMS['PAIR']}\nsize: {entry_amount}\npurchase price: {ticker['lowestAsk']} ")
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


def s3_logger(message):
    if message is not None:
        s3 = boto3.resource(
            's3',
            region_name=INFRASTRUCTURE_PARAMS['AWS_REGION'],
            aws_access_key_id=os.getenv('AWS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET')
        )
        object = s3.Object(
            INFRASTRUCTURE_PARAMS['S3_BUCKET_NAME'],
            'cmo_trading_strategy_audit/.txt'
        )
        response = object.put(Body=message)
    else:
        response = 'no trades'
    return response


def lambda_handler(event, context):

    poloniex_wrapper = Poloniex(
        APIKey=os.getenv('API_KEY'),
        Secret=os.getenv('SECRET')
    )

    base_currency = LOGICAL_PARAMS['PAIR'].split('_')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('_')[1]
    assert base_currency+'_'+quote_currency == LOGICAL_PARAMS['PAIR']

    cmo = check_cmo()

    if cmo < LOGICAL_PARAMS["OVERSOLD_VALUE"]:
        response = close_positions(poloniex_wrapper, base_currency)
    elif cmo > LOGICAL_PARAMS["OVERBOUGHT_VALUE"]:
        response = enter_position(poloniex_wrapper, base_currency, quote_currency)
    else:
        response = None

    s3_response = s3_logger(message=response)
    print(s3_response)


if __name__ == '__main__':
    lambda_handler(0, 0)