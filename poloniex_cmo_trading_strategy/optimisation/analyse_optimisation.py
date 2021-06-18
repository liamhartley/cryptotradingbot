import pandas as pd
import pandasql as ps

filepath = '/Users/liamhartley/PycharmProjects/cryptotradingbot/poloniex_cmo_trading_strategy/optimisation/optimisation_results.csv'

if __name__ == '__main__':
    df = pd.read_csv(filepath, header=0)
    optimised_df = ps.sqldf('select * from df order by net_profit')
    print(df)
