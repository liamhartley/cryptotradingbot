LOGICAL_PARAMS = {
    "CMO_PERIOD": 10,  # number of days that CMO is calculated over
    "PERIOD": 14400,  # period that data is received
    "PAIR": "ETH-USDC",  # crypto pair to trade
    "OVERSOLD_VALUE": -50,  # CMO threshold value to buy at
    "OVERBOUGHT_VALUE": 50,  # CMO threshold value to sell at
    "DRY_RUN": True,  # when True the bot will not execute trades
    "INITIAL_CAPITAL": 1000,  # currency at deployment (in quote currency)
    "ENTRY_SIZE": 0.1  # size of trade to buy/sell (e.g. 0.1=10% of INITIAL_CAPITAL)
}
