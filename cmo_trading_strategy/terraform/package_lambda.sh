#!/usr/local/bin bash
echo $BASH_VERSION

# run this script in the root directory (cryptotradingbot) to package all scripts and packages for the lambda deployment

# TODO terraform init and plan

# scripts required and payload directory destinations

########## personal laptop paths ##########
#declare -A scripts=(
#                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/app.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/"
#                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/backtesting/backtesting.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/cmo_trading_strategy/backtesting/"
#                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/config.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/cmo_trading_strategy/config/"
#                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/poloniex_wrapper_bwentzloff.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/trading_tools/"
#                  ["/Users/liamhartley/PycharmProjects/Gemini/gemini/helpers/poloniex.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/gemini/helpers/"
## had to copy pandas in manually (script needs updating) ["/Users/liamhartley/PycharmProjects/cryptotradingbot/venv/lib/python3.9/site-packages/pandas/*"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/gemini/helpers/pandas"
#                  )
#
## copy all scripts into the payload directory
#for script in "${!scripts[@]}"
#do
#  mkdir -p "${scripts[$script]}"
#  cp "$script" "${scripts[$script]}"
#  echo "copied $script into ${scripts[$script]}"
#done
#
#
#### zipping ###
#echo "zipping"
#zip_destination_location="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload.zip"
#payload_location="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/"
#
#cd "$payload_location" || exit
#zip -r "$zip_destination_location" *


########## work laptop paths ##########
declare -A scripts=(
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/app.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/"
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/config.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/cmo_trading_strategy/"
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_tools/poloniex_wrapper_bwentzloff.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/trading_tools/"
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_tools/cmo_calculation.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/trading_tools/"
                  )
# had to copy pandas in manually (script needs updating) ["/Users/liamhartley/PycharmProjects/cryptotradingbot/venv/lib/python3.9/site-packages/pandas/*"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/gemini/helpers/pandas"

# copy all scripts into the payload directory
for script in "${!scripts[@]}"
do
  mkdir -p "${scripts[$script]}"
  cp "$script" "${scripts[$script]}"
  echo "copied $script into ${scripts[$script]}"
done


### zipping ###
echo "zipping"
zip_destination_location="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload.zip"
payload_location="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cmo_trading_strategy/app/payload/"

cd "$payload_location" || exit
zip -r "$zip_destination_location" *
