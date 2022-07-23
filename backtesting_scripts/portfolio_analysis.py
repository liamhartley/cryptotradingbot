import csv
import os
import time
import pandas as pd


def bulk_data_transform(data_location):
    '''
    write a function that iterates through every file in a folder to perform an operation.
    Lambda function???
    :param data_location:
    :return:
    '''
    for file in os.getcwd():
        return


def single_day(raw_path, output_path, day_of_week):
    df = pd.read_csv(raw_path)
    with open(output_path, 'w') as f:
        f.write('unix,date,symbol,open,high,low,close,Volume BNB,Volume USDT,tradecount\n')
        for index, row in df.iterrows():
            date = time.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
            if date.tm_wday == day_of_week:
                writer = csv.DictWriter(f, list(dict(row).keys()))
                writer.writerow(dict(row))


if __name__ == '__main__':
    data_filepath = '/Users/liam.hartley/PycharmProjects/cryptotradingbot/backtesting_raw_data/daily_binance/Binance_BTCUSDT_d.csv'
    bulk_data_transform('/Users/liam.hartley/PycharmProjects/cryptotradingbot/backtesting_raw_data/daily_binance/')
    single_day(raw_path=data_filepath, output_path=f'{data_filepath}_transformed.csv', day_of_week=0)
