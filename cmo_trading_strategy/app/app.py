from gemini.helpers import poloniex
from cmo_trading_strategy.backtesting.backtesting import cmo_logic
from cmo_trading_strategy.config import LOGICAL_PARAMS

PAIR = "BTC_USDT"
PERIOD = 86400


def check_cmo():

    past_data = poloniex.load_dataframe(
        pair=LOGICAL_PARAMS["BTC_USDT"],
        period=LOGICAL_PARAMS["PERIOD"],
        days_history=LOGICAL_PARAMS["CMO_PERIOD"]
    )

    if len(past_data)+1 == LOGICAL_PARAMS["CMO_PERIOD"]:
        past_data = past_data[1:]
    elif len(past_data) == LOGICAL_PARAMS["CMO_PERIOD"]:
        pass
    else:
        raise Exception("Invalid CMO check")
    cmo = cmo_logic(past_data)
    return cmo

def close_positions():


def lambda_handler(event, context):
    cmo = check_cmo()
    if cmo < OVERSOLD_VALUE:
        close positions
    elif cmo > OVERBOUGHT_VALUE:
        enter position
    else:
        log nothing to do

#  Calculate CMO
#  Check to see if we should close any positions
#  Check to see if we need to open any new positions


if __name__ == '__main__':
    lambda_handler(0, 0)
