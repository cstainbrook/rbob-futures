import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def create_futures_df(raw_data_path):

    shell_df = pd.DataFrame(columns=['front_month', 'second_month'])
    first_df = pd.read_csv(os.path.join(raw_data, 'XBWF_1987_Comdty.csv'))
    first_df.set_index('date', inplace=True)
    first_df.index = pd.to_datetime(first_df.index)
    shell_df['front_month'] = first_df['close']
    second_df = pd.read_csv(os.path.join(raw_data, 'XBWG_1987_Comdty.csv'))
    second_df.set_index('date', inplace=True)
    second_df.index = pd.to_datetime(second_df.index)
    shell_df['second_month'] = second_df['close']
    last_expiry = shell_df.index[-1]
    new_front_df = second_df.loc[last_expiry:].iloc[1:]
    new_front_df.columns = ['0', 'front_month']
    shell_df = shell_df.reset_index().merge(new_front_df.reset_index(), how='outer').set_index('date')

    for year in np.arange(1987,2019):
        for month in ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'X', 'Z']:
            print year
            temp_df = pd.read_csv(os.path.join(raw_data, 'XBW{}_{}_Comdty.csv'.format(month, year)))
            temp_df.set_index('date', inplace=True)
            temp_df.index = pd.to_datetime(temp_df.index)
            new_second_month_df = temp_df.loc[last_expiry:shell_df.index[-1]].iloc[1:]
            new_second_month_df.columns = ['0', 'second_month']
            shell_df.loc[shell_df.loc[last_expiry:].iloc[1:].index, 'second_month'] = new_second_month_df['second_month']
            last_expiry = shell_df.index[-1]
            new_front_df = temp_df.loc[last_expiry:].iloc[1:]
            new_front_df.columns = ['0', 'front_month']
            shell_df = shell_df.reset_index().merge(new_front_df.reset_index(), how='outer').set_index('date')

    shell_df.drop('0', axis=1, inplace=True)
    shell_df.dropna(inplace=True)

    return shell_df

if __name__ == "__main__":
    home = os.path.expanduser('~')
    desktop = os.path.join(home, 'Desktop')
    rbob_dir = os.path.join(desktop, 'rbob-futures')
    raw_data = os.path.join(rbob_dir, 'raw-futures-data')

    futures_df = create_futures_df(raw_data)


    F = Jan
    G = Feb
    H = March
    J = Apr
    K = May
    M = June
    N = July
    Q = Aug
    U = Sept
    X = Nov
    Z = Dec
