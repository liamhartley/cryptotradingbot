import time
import requests
import datetime
from trading_strategies.coinbase_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_tools.coinbase_pro_wrapper.public_client import PublicClient


def coinbase_cmo_logic_no_pandas(pair: str, period: int):
    '''
    Calulcate CMO over a given period for a given pair and CMO period.
    :param pair: currency pair to trade
    :param period: time period, NOT CMO period
    :return:
    '''
    datetime.datetime.now().isoformat()
    start_time = (datetime.datetime.now() - datetime.timedelta(seconds=LOGICAL_PARAMS['PERIOD']) - datetime.timedelta(seconds=LOGICAL_PARAMS['PERIOD'] * LOGICAL_PARAMS['CMO_PERIOD'])).isoformat()
    response_json = PublicClient().get_product_historic_rates(product_id=pair, granularity=period, start=start_time, end=datetime.datetime.now().isoformat())

    print(f'historical data: {response_json}')

    higher_close_price = 0
    lower_close_price = 0

    previous_day = False

    for day in response_json:
        if previous_day is not False:
            if day[4] > previous_day[4]:
                lower_close_price += day[4] - previous_day[4]
            elif day[4] < previous_day[4]:
                higher_close_price += previous_day[4] - day[4]
        previous_day = day

    cmo = ((higher_close_price - lower_close_price) / (higher_close_price + lower_close_price)) * 100
    print(f'higher_close_price: {higher_close_price}')
    print(f'lower_close_price: {lower_close_price}')
    return cmo


if __name__ == '__main__':
    coinbase_cmo_logic_no_pandas(pair='ETH-USDC', period=21600)
