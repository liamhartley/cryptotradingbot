import time

import pandas as pd

from gemini.gemini_core.gemini_master import Gemini
from gemini.helpers import poloniex, analyze
from trading_tools.coinbase_cmo_calculation import coinbase_cmo_logic_no_pandas
from trading_strategies.coinbase_cmo_trading_strategy.config import LOGICAL_PARAMS
from trading_tools.coinbase_pro_wrapper.public_client import PublicClient
from trading_tools.poloniex_cmo_calculation import poloniex_cmo_logic_no_pandas

# PERIOD_DICTIONARY = {86400: '1D', 21600: '6H', 3600: '1H', 900: '0.25H', 300: '5M', 60: '1M'}
PERIOD_DICTIONARY = {86400: '1D'}
poloniex_period = 86400
# PERIOD_DICTIONARY = {86400: '1D', 14400: '4H', 7200: '2H', 1800: '0.5H', 900: '0.25H'}  # Poloniex API
# PERIOD_DICTIONARY = {86400: '1D', 7200: '2H'}  # Poloniex API

OUTPUT_FILEPATH = 'C:/Users/doseo/PycharmProjects/cryptotradingbot/output.csv'
CMO_PERIODS = [7]
# CMO_PERIODS = [10, 11, 12]
DAYS_HISTORY = 5
OVERBOUGHT_VALUEs = [40]
OVERSOLD_VALUEs = [-60]
CAPITAL_BASE = 1000
ENTRY_SIZE_LIST = [CAPITAL_BASE*0.05]

# PAIRS = ['ETH_USDC', 'USDC_SOL']
# PAIRS = ['ETH-USDC', 'SOL-USDC']
PAIRS = ['ETH-USDC']
# PAIRS = ['ETH_USDC']
# PAIRS = ['SOL_USDT']

# PAIRS = ['XRP_BTC']
# PAIRS = ['AMP_USDT']
# PAIRS = ['BTC_XRP']

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

def jaz_trading(gemini, data):
    if data.iloc[-1]["open"] > 3000:
        gemini.account.enter_position(type_="Long",
                                      entry_capital=ENTRY_SIZE,
                                      entry_price=data.iloc[-1]['high'])
        print(f'Open position @ {data.iloc[-1]["low"]}')
    elif data.iloc[-1]["open"] < 3000:
         gemini.account.close_position(position=gemini.account.positions[0],
                                      percent=1,
                                      price=data.iloc[-1]['low'])
         print(f'Close position @ {data.iloc[-1]["low"]}')

def cmo_trading_strategy(gemini, data):
    base_currency = LOGICAL_PARAMS['PAIR'].split('-')[0]
    quote_currency = LOGICAL_PARAMS['PAIR'].split('-')[1]
    if len(data) >= CMO_PERIOD:
        # cmo = poloniex_cmo_logic_no_pandas(pair=quote_currency+'_'+base_currency, period=api_period)
        cmo = coinbase_cmo_logic_no_pandas(pair=LOGICAL_PARAMS['PAIR'], period=api_period)
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
    total_simulations = len(PAIRS) * len(PERIOD_DICTIONARY) * len(CMO_PERIODS) * len(ENTRY_SIZE_LIST) * len(OVERSOLD_VALUEs) * len(OVERSOLD_VALUEs)
    print(f'Total backtesting simulations: {total_simulations}\n')
    time.sleep(1)

    for PAIR in PAIRS:
        # PAIR = PAIR[:-1]
        for OVERSOLD_VALUE in OVERSOLD_VALUEs:
            for OVERBOUGHT_VALUE in OVERBOUGHT_VALUEs:
                for api_period, gemini_period in PERIOD_DICTIONARY.items():
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
                                    'Long': 0.005,  # as a percentage
                                    'Short': 0.005
                                }
                            }

                            # load backtesting data
                            # data_df = poloniex.load_dataframe(pair=PAIR, period=poloniex_period, days_history=DAYS_HISTORY)
                            data = PublicClient().get_product_historic_rates(product_id=PAIR, granularity=poloniex_period)
                            headers = ['time', 'low', 'high', 'open', 'close', 'volume'],
                            df = pd.DataFrame(data)
                            df.columns = headers[0]
                            df['time'] = pd.to_datetime(df['time'], unit='s')
                            df = df.set_index('time')
                            df = df.reindex(columns=['high', 'low', 'open', 'close', 'volume'])

                            backtesting_engine = Gemini(logic=jaz_trading, sim_params=params, analyze=analyze.analyze_bokeh)

                            # run the backtesting engine
                            backtesting_engine.run(data=df)

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
