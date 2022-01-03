#!/usr/local/bin bash
echo $BASH_VERSION

# Set the name of your custom workspace
workspace_name="coinbase-cmo"

# run this script in the root directory after defining the filepaths below to deploy your trading strategy
lambda_zip_filepath="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload.zip"
payload_filepath="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/"
infrastructure_filepath="/Users/liamhartley/PycharmProjects/cryptotradingbot/cloud_infrastructure/aws_terraform/"

# TODO automate these paths or move this config into each strategy
# TODO make this its own function
########## required trading script paths ##########
declare -A scripts=(
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/app.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/config.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/trading_strategies/coinbase_cmo_trading_strategy/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/coinbase_cmo_calculation.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/trading_tools/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/coinbase_pro_wrapper/authenticated_client.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/trading_tools/coinbase_pro_wrapper/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/coinbase_pro_wrapper/public_client.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/trading_tools/coinbase_pro_wrapper/"
                  ["/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_tools/coinbase_pro_wrapper/cbpro_auth.py"]="/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/app/payload/trading_tools/coinbase_pro_wrapper/"
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

### deploying cloud infrastructure ###
echo "deploying cloud infrastructure"
cd $infrastructure_filepath || exit

# update the backend config to point to the respective workspace
terraform workspace new $workspace_name || echo "Workspace $workspace_name already exists"
terraform workspace select $workspace_name

terraform init


terraform apply -lock=false
