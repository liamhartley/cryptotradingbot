# Poloniex CMO Trading Strategy

## Contents
0. [Overview](#overview)
1. [Project Architecture](#projectarchitecture)
2. [Setup](#setup) 
3. [Usage](#usage)
4. [How to Contribute](#howtocontribute)
5. [Further Reading](#furtherreading)
6. [Acknowledgements](#acknowledgements)
7. [Donations](#donations)

<a name="overview"></a>
## Overview 

This solution allows you to run the strategy 24/7 on AWS.

You can watch the entire development of this project on [this YouTube playlist](https://www.youtube.com/watch?v=ee0JCfeFw1o&list=PLobCEGRAX3hZ0KqKoZ1RTlYZF-VguIhtC&index=4).
You can see this project being deployed in [this video](https://www.youtube.com/watch?v=ee0JCfeFw1o&list=PLobCEGRAX3hZ0KqKoZ1RTlYZF-VguIhtC&index=3). 

The trading strategy uses CMO to analyse when there is potentially too much trading momentum in one direction.

If the asset is considered to be oversold (CMO < oversold threshold) then the bot will purchase the amount defined in the config file.

The opposite is also true, overbought assets (CMO > overbought threshold) will cause the bot to sell an amount defined in the config. 

<a name="projectarchitecture"></a>
## Project Architecture 

<img src="https://github.com/liamhartley/cryptotradingbot/blob/master/poloniex_cmo_trading_strategy/docs/cmo_trading_architecture.png" width="500px">

---

- Terraform deploys all of the infrastructure into AWS
- Cloudwatch is the trigger which kicks off the Lambda function
- The Lambda function contains the trading logic which is written in Python
- This logic uses the Poloniex API to connect to the exchange
- Every decision that the Lambda takes is logged into an S3 bucket for auditing

---

<a name="setup"></a>
## Setup 


#### Pre-Requisites

- [Python version 3.0.0 and above](https://www.python.org/downloads/) for backtesting and optimisation.
- [Terraform version 0.13.0 and above](https://www.terraform.io/downloads.html) for cloud infrastructure deployment.
- An [AWS](https://aws.amazon.com) account.
- Packages inside the requirements.txt file.

To install requirements file (inside project root): `pip install  -r requirements.txt`

To upgrade to the latest backtesting package: `pip install  git+https://github.com/liamhartley/Gemini.git --upgrade`


<a name="usage"></a>
## Usage 

#### Terraform AWS Deployment

All of the AWS resources are managed by Terraform and it is best practice to make changes to the code and re-deploy instead of making changes in the GUI.

- Create a terraform.tfvars file in the terraform directory to store your environment variables (defined in variables.tf in the Terraform folder)
- Modify the filepaths in the "package_lambda.sh" script in <strategy>/terraform for your machine
- Navigate to the root directory of the project in the terminal
- Run the "package_lambda.sh" script in <strategy>/terraform
- Run Terraform init in the terraform directory to download the required modules
- Run Terraform plan in the Terraform directory to ensure that your plan is working as expected
- Run Terraform apply in the Terraform directory to deploy the cloud infrastructure

All logs will be outputted to Cloudwatch and the respective S3 bucket for debugging.

#### Backtesting

If you wish to re-run the backtesting/optimisation to identify which cryptocurrency pair you would like to trade then navigate to the backtesting.py script in the backtesting folder.
Change the filepath of the csv output in the __main__ function to a local filepath and modify the config in the strategies root folder.
Then run the backtesting with any permutation of the variables to build a dataset for optimisation.

#### Optimisation

Navigate to the analyse_optimisation.py script in the optimisation folder and change the filepath to be the same as the filepath in the optimsiation script.
Then run any SQL query you like against this dataframe to identify the most suitable trading configuration.

<a name="howtocontribute"></a>
## How to Contribute 

Branch off from the project to create a new feature and open a PR against master when complete. 

Please feel free to reach out to me to check if a feature isn't already in development.

<a name="projectarchitecture"></a>
## Further Reading
- Read more about the project [my blog](https://medium.datadriveninvestor.com/deploying-a-bitcoin-trading-bot-eb9998dfc0f5)
- [CMO by Investopedia](https://www.investopedia.com/terms/c/chandemomentumoscillator.asp)
- [Poloniex Exchange](https://poloniex.com)

<a name="acknowledgements"></a>
## Acknowledgements 
- [The Gemini crypto backtesting engine](https://github.com/anfederico/Gemini) by anfederico 
- [The Poloniex wrapper](https://github.com/bwentzloff/trading-bot) by bwentzloff

<a name="donations"></a>
## Donations 

If this project helped you learn Python or has helped you make some money then I would love any tips in Dogecoin!

**My wallet address is**: DS7JRhMmL9RdXruqz5ubDaR3R8SNtoUi6i

[Alternatively you can buy me a coffee!](https://www.buymeacoffee.com/liamhartley)

