# Example config file to define your parameters across backtesting, optimisation and deployment

LOGICAL_PARAMS = {
    "PERIOD": 86400,
    "PAIR": "BTC_XRP",
    "DRY_RUN": True,
    "INITIAL_CAPITAL": 100,  # in quote currency
    "ENTRY_SIZE": 0.1  # 10%
}

INFRASTRUCTURE_PARAMS = {
    "S3_BUCKET_NAME": "",
    "AWS_REGION": "eu-west-1"
}
