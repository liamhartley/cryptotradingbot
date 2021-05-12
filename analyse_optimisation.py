import pandas as pd
import pandasql as ps

if __name__ == '__main__':
    df = pd.read_csv('/Users/liamhartley/PycharmProjects/cryptotradingbot/optimisation_results.csv', header=0)
    ps.sqldf('select * from df order by net_profit')
    print(df)