LOGICAL_PARAMS = {
    "CMO_PERIOD": 9,
    "PERIOD": 86400,
    "PAIR": "BTC_USDT",
    "OVERSOLD_VALUE": -50,
    "OVERBOUGHT_VALUE": 50,
    "DRY_RUN": True,
    "INITIAL_CAPITAL": 100,  # in quote currency
    "ENTRY_SIZE": 0.1  # 10%
}

INFRASTRUCTURE_PARAMS = {
    "S3_BUCKET_NAME": "cryptotradingbot-liamhartley",
    "AWS_REGION": "eu-west-2"
}
