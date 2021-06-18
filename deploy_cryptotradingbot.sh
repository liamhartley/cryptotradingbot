#!/usr/local/bin bash
echo $BASH_VERSION
# TODO finish the terraform deployment and redeploy the poloniex strategy

# run this script in the root directory after defining the filepaths below to deploy your trading strategy
lambda_zip_filepath="/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload.zip"
payload_filepath="/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/"
infrastructure_filepath="/Users/liam.hartley/PycharmProjects/cryptotradingbot/cloud_infrastructure/terraform/"
export strategy_name="poloniex_cmo"


# TODO run this script in the root directory (cryptotradingbot) to package all scripts and packages for the lambda deployment

# TODO automate these paths or move this config into each strategy
########## required trading script paths ##########
declare -A scripts=(
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/app.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/"
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/config.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/cmo_trading_strategy/"
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_tools/poloniex_wrapper_bwentzloff.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/trading_tools/"
                  ["/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_tools/cmo_calculation.py"]="/Users/liam.hartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/trading_tools/"
                  )

# copy all scripts into the payload directory
for script in "${!scripts[@]}"
do
  mkdir -p "${scripts[$script]}"
  cp "$script" "${scripts[$script]}"
  echo "copied $script into ${scripts[$script]}"
done

### zipping ###
echo "zipping"
cd $payload_filepath || exit
zip -r $lambda_zip_filepath ./*glob*

# TODO
### deploying cloud infrastructure ###
echo "deploying cloud infrastructure"
cd $infrastructure_filepath || exit

