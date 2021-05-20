#!/usr/bin/env bash

# run this script in the root directory to package all scripts and packages for the lambda deployment

#terraform init

# TODO

# packages
#cp -r /Users/liamhartley/IdeaProjects/fpl/venv/lib/python3.7/site-packages/spotipy ../lambda_payloads/avg_album_length_playlist_payload/

# scripts
cp /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/backtesting/backtesting.py /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/cmo_trading_strategy/backtesting/backtesting/
cp /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/app.py /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/
cp /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/config.py /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/cmo_trading_strategy/config/
cp /Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_tools/poloniex_wrapper_bwentzloff.py /Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/trading_tools/


cd ../lambda_payloads/avg_album_length_playlist_payload/

zip -r ../../payload.zip *

cd ../../.tf/

terraform plan

