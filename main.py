from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

# TODO optimise params
CMO_PERIOD = 9
PAIR = "BTC_USDT"
PERIOD = 1800
DAYS_HISTORY = 100

OVERBOUGHT_VALUE = 50
OVERSOLD_VALUE = -50

params = {
    'capital_base': 1000,
    'data_frequency': 'D',
    'fees': {
        'open_fee': 0.0001,
        'close_fee': 0.0001
    }
}


def cmo_logic(data):
    last_day = len(data)
    first_day = len(data) - CMO_PERIOD

    higher_close_price = 0
    lower_close_price = 0

    for ticker in range(first_day, last_day):
        if data['close'][ticker] > data['open'][ticker]:
            higher_close_price += 1
        elif data['close'][ticker] < data['open'][ticker]:
            lower_close_price += 1

    cmo = ((higher_close_price - lower_close_price) / (higher_close_price + lower_close_price)) * 100

    return cmo


def cmo_trading_strategy(gemini, data):
    if len(data) >= CMO_PERIOD:
        cmo = cmo_logic(data)
        assert -100 <= cmo <= 100

        if cmo < OVERSOLD_VALUE:
            gemini.account.close_position(position=gemini.account.positions[0],
                                          percent=1,
                                          price=data.iloc[-1]['low'])
        elif cmo > OVERBOUGHT_VALUE:
            gemini.account.enter_position(type_="Long",
                                          entry_capital=params['capital_base']*0.1,
                                          entry_price=data.iloc[-1]['high'])
        else:
            raise Exception


if __name__ == '__main__':
    data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    backtesting_engine = Gemini(logic=cmo_trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)
    backtesting_engine.run(data=data_df)

