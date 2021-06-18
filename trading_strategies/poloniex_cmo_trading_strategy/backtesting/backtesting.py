from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze

CMO_PERIOD = 14

PERIOD = 1800
DAYS_HISTORY = 100
OVERBOUGHT_VALUE = 50
OVERSOLD_VALUE = -50

params = {
    'capital_base': 10,
    'data_frequency': 'D',
    'fees': {
        'open_fee': 0.00125,  # as a percentage
        'close_fee': 0.00125
    }
}

# ENTRY_SIZES = [params['capital_base']*0.05,params['capital_base']*0.1,params['capital_base']*0.15,params['capital_base']*0.2]
ENTRY_SIZE = params['capital_base']*0.1

PAIRS = [
    'BTC_USDT\n',
    'DOGE_BTC\n',
    'ETH_USDT\n',
    'DOGE_USDT\n',
    'ETH_BTC\n',
    'XRP_USDT\n',
    'TRX_USDT\n',
    'BTC_USDC\n',
    'XRP_BTC\n',
    'LTC_USDT\n',
    'SRM_USDT\n',
    'XMR_BTC\n',
    'LTC_BTC\n',
    'TRX_BTC\n',
    'ETC_USDT\n',
    'ETH_USDC\n',
    'ATOM_BTC\n',
    'EOS_BTC\n',
    'XEM_BTC\n',
    'EOS_USDT\n',
    'BCH_USDT\n',
    'ETC_BTC\n',
    'BCH_BTC\n',
    'XMR_USDT\n',
    'ATOM_USDC\n',
    'DOT_USDT\n',
    'ATOM_USDT\n',
    'BNB_USDT\n',
    'USDT_USDC\n',
    'USDJ_USDT\n',
    'DOGE_USDC\n',
    'SC_USDT\n',
    'EOS_USDC\n',
    'LSK_BTC\n',
    'BTT_USDT\n',
    'DASH_BTC\n',
    'TUSD_USDT\n',
    'BCH_USDC\n',
    'AMP_USDT\n',
    'XRP_USDC\n',
    'JST_USDT\n',
    'DASH_USDT\n',
    'ETC_ETH\n',
    'ZEC_USDT\n',
    'KCS_USDT\n',
    'QTUM_BTC\n',
    'LSK_USDT\n',
    'SC_BTC\n'
]


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

        if cmo < OVERSOLD_VALUE:
            gemini.account.enter_position(type_="Long",
                                          entry_capital=ENTRY_SIZE,
                                          entry_price=data.iloc[-1]['high'])
        elif cmo > OVERBOUGHT_VALUE:
            gemini.account.close_position(position=gemini.account.positions[0],
                                          percent=1,
                                          price=data.iloc[-1]['low'])
        else:
            print('No trade')


if __name__ == '__main__':

    for PAIR in PAIRS:
        PAIR = PAIR[:-1]
        # load backtesting data
        data_df = poloniex.load_dataframe(pair=PAIR, period=PERIOD, days_history=DAYS_HISTORY)

        backtesting_engine = Gemini(logic=cmo_trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)

        # run the backtesting engine
        backtesting_engine.run(data=data_df)

        backtesting_engine.save_results_to_csv(
            filepath='/Users/liamhartley/PycharmProjects/cryptotradingbot/poloniex_cmo_trading_strategy/optimisation/optimisation_results.csv',
            additional_datapoints=[PAIR,
                                   CMO_PERIOD,
                                   OVERSOLD_VALUE,
                                   OVERBOUGHT_VALUE,
                                   ENTRY_SIZE,
                                   ]
        )
