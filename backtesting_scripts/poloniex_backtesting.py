import time
from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze


# PERIOD_DICTIONARY = {7200: '2H'}
PERIOD_DICTIONARY = {86400: '1D', 14400: '4H', 7200: '2H', 1800: '0.5H', 900: '0.25H'}
OUTPUT_FILEPATH = '/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/optimisation/sol_optimisation.csv'
CMO_PERIODS = [7, 8, 9, 10]
DAYS_HISTORY = 180
OVERBOUGHT_VALUE = 50
OVERSOLD_VALUE = -50
CAPITAL_BASE = 1000
ENTRY_SIZE_LIST = [CAPITAL_BASE*0.1, CAPITAL_BASE*0.15, CAPITAL_BASE*0.2, CAPITAL_BASE*0.25, CAPITAL_BASE*0.30,
                   CAPITAL_BASE*0.35, CAPITAL_BASE*0.40, CAPITAL_BASE*0.45, CAPITAL_BASE*0.5, CAPITAL_BASE*0.55]

# PAIRS = ['XRP_BTC']
# PAIRS = ['AMP_USDT']
PAIRS = ['SOL_USDT']

# PAIRS = [
#     'BTC_USDT\n',
#     'DOGE_BTC\n',
#     'ETH_USDT\n',
#     'DOGE_USDT\n',
#     'ETH_BTC\n',
#     'XRP_USDT\n',
#     'TRX_USDT\n',
#     'BTC_USDC\n',
#     'XRP_BTC\n',
#     'LTC_USDT\n',
#     'SRM_USDT\n',
#     'XMR_BTC\n',
#     'LTC_BTC\n',
#     'TRX_BTC\n',
#     'ETC_USDT\n',
#     'ETH_USDC\n',
#     'ATOM_BTC\n',
#     'EOS_BTC\n',
#     'XEM_BTC\n',
#     'EOS_USDT\n',
#     'BCH_USDT\n',
#     'ETC_BTC\n',
#     'BCH_BTC\n',
#     'XMR_USDT\n',
#     'ATOM_USDC\n',
#     'DOT_USDT\n',
#     'ATOM_USDT\n',
#     'BNB_USDT\n',
#     'DOGE_USDC\n',
#     'SC_USDT\n',
#     'EOS_USDC\n',
#     'LSK_BTC\n',
#     'BTT_USDT\n',
#     'DASH_BTC\n',
#     'TUSD_USDT\n',
#     'BCH_USDC\n',
#     'AMP_USDT\n',
#     'XRP_USDC\n',
#     'JST_USDT\n',
#     'DASH_USDT\n',
#     'ETC_ETH\n',
#     'ZEC_USDT\n',
#     'KCS_USDT\n',
#     'QTUM_BTC\n',
#     'LSK_USDT\n',
#     'SC_BTC\n'
# ]


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
            print(f'Open position @ {data.iloc[-1]["low"]}')
        elif cmo > OVERBOUGHT_VALUE and len(gemini.account.positions) > 0:
            gemini.account.close_position(position=gemini.account.positions[0],
                                          percent=1,
                                          price=data.iloc[-1]['low'])
            print(f'Close position @ {data.iloc[-1]["low"]}')


if __name__ == '__main__':
    total_simulations = len(PAIRS) * len(PERIOD_DICTIONARY) * len(CMO_PERIODS) * len(ENTRY_SIZE_LIST)
    print(f'Total backtesting simulations: {total_simulations}\n')
    time.sleep(5)

    for PAIR in PAIRS:
        # PAIR = PAIR[:-1]
        for poloniex_period, gemini_period in PERIOD_DICTIONARY.items():
            for cmo_period in CMO_PERIODS:
                global CMO_PERIOD
                CMO_PERIOD = cmo_period
                for entry_size in ENTRY_SIZE_LIST:
                    global ENTRY_SIZE
                    ENTRY_SIZE = entry_size
                    print(f"Pair: {PAIR}")
                    params = {
                        'capital_base': CAPITAL_BASE,
                        'data_frequency': gemini_period,
                        'fee': {
                            'Long': 0.00125,  # as a percentage
                            'Short': 0.00125
                        }
                    }

                    # load backtesting data
                    data_df = poloniex.load_dataframe(pair=PAIR, period=poloniex_period, days_history=DAYS_HISTORY)

                    backtesting_engine = Gemini(logic=cmo_trading_strategy, sim_params=params, analyze=analyze.analyze_bokeh)

                    # run the backtesting engine
                    backtesting_engine.run(data=data_df)

                    backtesting_engine.save_results_to_csv(
                        filepath=OUTPUT_FILEPATH,
                        additional_datapoints=[PAIR,
                                               CMO_PERIOD,
                                               OVERSOLD_VALUE,
                                               OVERBOUGHT_VALUE,
                                               ENTRY_SIZE,
                                               poloniex_period
                                               ]
                    )
