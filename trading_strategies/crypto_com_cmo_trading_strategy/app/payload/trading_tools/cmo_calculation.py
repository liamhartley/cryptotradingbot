import time
import requests
from trading_strategies.poloniex_cmo_trading_strategy.config import LOGICAL_PARAMS


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


def cmo_logic_no_pandas():
    response_json = get_past(
        pair=LOGICAL_PARAMS["PAIR"],
        period=LOGICAL_PARAMS["PERIOD"],
        days_history=LOGICAL_PARAMS["CMO_PERIOD"]
    )

    print(f'historical data: {response_json}')

    # if len(response_json)-1 == LOGICAL_PARAMS["CMO_PERIOD"]:
    #     past_data = response_json[1:]
    # elif len(response_json) == LOGICAL_PARAMS["CMO_PERIOD"]:
    #     past_data = response_json
    # else:
    #     raise Exception("Invalid CMO check")

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
    cmo_logic_no_pandas()
