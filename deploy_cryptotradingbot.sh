#!/usr/local/bin bash
echo $BASH_VERSION

# run this script in the root directory after defining the filepaths below to deploy your trading strategy
lambda_zip_filepath="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload.zip"
payload_filepath="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/"
infrastructure_filepath="/Users/liamhartley/PycharmProjects/cryptotradingbot/cloud_infrastructure/aws_terraform/"

export TF_VAR_PROJECT_NAME="poloniex-cmo"
export TF_VAR_PAYLOAD_FUNCTION_FILEPATH="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload.zip"
export TF_VAR_TRADING_FREQUENCY="rate(1 hour)" # currently configured to be one frequency per strategy


# TODO automate these paths or move this config into each strategy
# TODO make this its own function
########## required trading script paths ##########
declare -A scripts=(
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/app.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/config.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/trading_strategies/poloniex_cmo_trading_strategy/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/poloniex_wrapper_bwentzloff.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/trading_tools/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/cmo_calculation.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/poloniex_cmo_trading_strategy/app/payload/trading_tools/"
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
zip -r $lambda_zip_filepath *

# TODO
### deploying cloud infrastructure ###
echo "deploying cloud infrastructure"
cd $infrastructure_filepath || exit

terraform init

terraform apply -lock=false
