from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

# TODO optimise params by looping through different values, currency pairs etc
CMO_PERIOD = 9
PAIR = "BTC_USDT"
PERIOD = 1800
DAYS_HISTORY = 100
OVERBOUGHT_VALUE = 50
OVERSOLD_VALUE = -50

params = {
    # TODO link
    'capital_base': 10,
    'data_frequency': 'D',
    # TODO check these
    'fees': {
        'open_fee': 0.0001,
        'close_fee': 0.0001
    }
}


def cmo_logic(data) -> float:
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

        # TODO optimise the params here
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
    # load backtesting data
    data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

    # load backtesting engine with your strategy
    backtesting_engine = Gemini(logic=cmo_trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)

    # run the backtesting engine
    backtesting_engine.run(data=data_df)

