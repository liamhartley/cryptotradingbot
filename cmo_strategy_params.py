from datetime import datetime as dt
today = dt.today()

cmo_params = {'CMO_PERIOD': 9,
              'CANDLE_PERIOD': 1800,
              'BACKTESTING_PAIRS': 'ETH_BTC',  # TODO check why we   can't pass the below into backtesting
              'PAIRS': 'BTC_ETH',
              'SAVE_DATA_LOCALLY': False,
              'OVERBOUGHT_VALUE(0:100)': 50,
              'OVERSOLD_VALUE(-100:0)': -50,
              'ASK_ADJUSTMENT': 1,
              'BID_ADJUSTMENT': 1,
              'MAX_POSITIONS': 5,
              'TRADE_SIZE': 0.2}

# Ask is what the seller is asking for
# Bid is how much someone is trying to buy for

cmo_aws_params = {'BUCKET_NAME': 'cmo-bitcoin-trading',
                  'KEY_PARTITIONS': f'bot_logging/year={str(today.year)}/month={str(today.month)}/day={str(today.day)}'}
