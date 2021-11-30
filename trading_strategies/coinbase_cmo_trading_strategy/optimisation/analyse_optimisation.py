import pandas as pd
import pandasql as ps

# 180 days multiple periods
filepath = '/Users/liamhartley/PycharmProjects/cryptotradingbot/trading_strategies/coinbase_cmo_trading_strategy/optimisation/backtesting_results.csv'


if __name__ == '__main__':
    df = pd.read_csv(filepath, header=0)
    optimised_df = ps.sqldf('select * from df order by net_profit desc')
    optimised_df_no_atom = ps.sqldf('select * from df where pair not like "ATOM%" order by net_profit desc')
    period_df = ps.sqldf('select poloniex_period, avg(net_profit) as net_profit, avg(sharpe_ratio),  sum(fees_paid), avg(total_trades) from df group by poloniex_period order by net_profit desc')
    period_df_profit = ps.sqldf('select poloniex_period, avg(net_profit) as net_profit, avg(sharpe_ratio),  sum(fees_paid), avg(total_trades) from df where net_profit > 0 group by poloniex_period order by net_profit desc')
    # df = df.drop(['cmo_period', 'oversold_value', 'overbought_value', 'entry_size', 'starting_capital'], axis=1)

    crypto_selection_df = ps.sqldf('select * from df where pair not like "ATOM%" and poloniex_period = 7200 order by net_profit desc')

    print(df)

    # # period analysis
    # ps.sqldf('select poloniex_period, avg(net_profit) as net_profit, avg(sharpe_ratio),  sum(fees_paid), avg(total_trades) from df group by poloniex_period order by net_profit desc')
