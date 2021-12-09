import time
import requests
from trading_strategies.poloniex_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_tools.coinbase_pro_wrapper.public_client import PublicClient


def coinbase_cmo_logic_no_pandas(pair: str, period: int):
    response_json = PublicClient().get_product_historic_rates(product_id=pair, granularity=period)

    print(f'historical data: {response_json}')

    higher_close_price = 0
    lower_close_price = 0

    previous_day = False

    for day in response_json:
        if previous_day is not False:
            if day[4] > previous_day[4]:
                higher_close_price += 1
            elif day[4] < previous_day[4]:
                lower_close_price += 1
        previous_day = day

    cmo = ((higher_close_price - lower_close_price) / (higher_close_price + lower_close_price)) * 100
    print(f'higher_close_price: {higher_close_price}')
    print(f'lower_close_price: {lower_close_price}')
    return cmo


if __name__ == '__main__':
    coinbase_cmo_logic_no_pandas(pair='ETH-USDC', period=21600)
