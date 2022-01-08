import time
import requests
# from trading_strategies.poloniex_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_strategies.coinbase_cmo_trading_strategy.config import LOGICAL_PARAMS


def get_past(pair, period, days_history=30):
    """
    Return historical charts data from poloniex.com
    :param pair:
    :param period:
    :param days_history:
    :return:
    """
    end = int(time.time())
    start = end - (24 * 60 * 60 * days_history)
    params = {
        'command': 'returnChartData',
        'currencyPair': pair,
        'start': start,
        'end': end,
        'period': period
    }

    response = requests.get('https://poloniex.com/public', params=params)
    return response.json()


def poloniex_cmo_logic_no_pandas(pair: str):
    response_json = get_past(
        pair=pair,
        period=LOGICAL_PARAMS["PERIOD"],
        days_history=LOGICAL_PARAMS["CMO_PERIOD"]
    )
    # Get the last x days of data with respect to the cmo period (-1s for 0 index and having one extra day)
    response_json = response_json[len(response_json) - 1 - LOGICAL_PARAMS["CMO_PERIOD"] - 1:len(response_json) - 1]
    print(f'historical data: {response_json}')

    higher_close_price = 0
    lower_close_price = 0

    previous_day = False

    for day in response_json:
        if previous_day is not False:
            if day['close'] > previous_day['close']:
                higher_close_price += 1
            elif day['close'] < previous_day['close']:
                lower_close_price += 1
        previous_day = day

    cmo = ((higher_close_price - lower_close_price) / (higher_close_price + lower_close_price)) * 100
    print(f'higher_close_price: {higher_close_price}')
    print(f'lower_close_price: {lower_close_price}')
    return cmo


if __name__ == '__main__':
    poloniex_cmo_logic_no_pandas()
