# Optimisation scripts analyse the data generated in backtesting
# See below for example on how to use SQL on a Pandas DataFrame

# import pandas as pd
# import pandasql as ps
#
# filepath = '/Users/liamhartley/PycharmProjects/cryptotradingbot/poloniex_cmo_trading_strategy/optimisation/initial_optimisation_results.csv'
#
# if __name__ == '__main__':
#     df = pd.read_csv(filepath, header=0)
#     optimised_df = ps.sqldf('select * from df order by net_profit')
#     print(df)
