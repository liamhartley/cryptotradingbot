# Crypto Trading Bot

## Contents
0. [Introduction](#introduction)
1. [Template Architecture](#architecture)
1. [Trading Strategies](#strategies)
1. [Usage](#usage)
2. [Future Improvements](#futureimprovements)
3. [How to Contribute](#howtocontribute)
4. [Further Reading](#furtherreading)
5. [Donations](#donations)

<a name="introduction"></a>
## Introduction 

A project to automatically run technical analysis strategies on AWS to trade cryptocurrencies whilst you sleep.

This project aims to have multiple trading strategies that can all be deployed into AWS using Terraform.

You can watch YouTube videos about the project [here](https://www.youtube.com/watch?v=ee0JCfeFw1o&list=PLobCEGRAX3hZ0KqKoZ1RTlYZF-VguIhtC&index=4) 

<a name="architecture"></a>
## Project Architecture

#### Repository Structure

- cloud_infrastructure: this folder contains all the infrastructure as code in order to deploy trading strategies.
- trading_strategies: each folder within trading_strategies contains all the code required to backtest, optimise and develop your trading logic. The "app" logic is what gets deployed in the generic setup.
- trading_tools: generic pieces of code that can be used across multiple trading strategies.

#### Generic Trading Architecture Overview (may differ between trading strategies)

- The cloud infrastructure is deployed and managed using infrastructure as code. In this example terraform deploys all the infrastructure into AWS.
- Cloudwatch (AWS) is the trigger which kicks off the Lambda Function (AWS) at a pre-defined frequency.
- The Lambda function contains the trading strategy to execute trades.
- Every decision that the Lambda takes is logged into to Cloudwatch for auditing.

<img src="https://github.com/liamhartley/cryptotradingbot/blob/master/project_architecture.png" width="500px">

<a name="strategies"></a>
## Trading Strategies

- [Polniex Chande Momentum Oscillator (CMO) Trading strategy](https://github.com/liamhartley/cryptotradingbot/blob/master/poloniex_cmo_trading_strategy/)

<a name="usage"></a>
## Usage 

Please see each trading strategies README for specific usage instructions:

- [Poloniex CMO Trading Strategy](https://github.com/liamhartley/cryptotradingbot/blob/master/poloniex_cmo_trading_strategy/README.md)


<a name="futureimprovements"></a>
## Future Improvements

Creation of more trading strategies.

Please contribute any trading strategies back into this repository.


<a name="howtocontribute"></a>
## How to Contribute 


Branch or fork off from the project to create a new feature and open a PR against master when complete.

Please feel free to reach out to me to check if a feature isn't already in development or raise issues on GitHub.

In the future I would love to see all sorts of strategies in this repo!

<a name="projectarchitecture"></a>
## Further Reading
- [CMO by Investopedia](https://www.investopedia.com/terms/c/chandemomentumoscillator.asp)
- [Poloniex Exchange](https://poloniex.com)

<a name="acknowledgements"></a>
## Acknowledgements 

- [The Gemini crypto backtesting engine](https://github.com/anfederico/Gemini) by anfederico 


<a name="donations"></a>
## Donations 

If this project helped you learn Python or has helped you make some money then I would love any tips in Dogecoin!

**My wallet address is**: DS7JRhMmL9RdXruqz5ubDaR3R8SNtoUi6i

[Alternatively you can buy me a coffee!](https://www.buymeacoffee.com/liamhartley)

