import pandas as pd
import glob
import os

parse_dates = ['DATETIME_SVR', 'DATETIME_ID']


def main():
    engine1()


def engine1():
    """ testing """

    file_path = "Green_log/er_3g_15min/dwhdb_MSK/*.res"
    datatype_dict = {'LAC': 'uint16', 'CELL_ID': 'uint16', "CDR": 'float16', "CDR_Attempts": 'uint16',
                     "CDR_Drops": 'uint16'}

    filelist = glob.glob(file_path)
    filelist.sort(key=os.path.getmtime)
    filelist = filelist[-6:]
    # print(filelist)

    df_from_each_file = (
        pd.read_csv(
            f,
            delimiter=';',
            decimal='.',
            header=0,
            index_col=["LAC", "CELL_ID", "CELL_NAME", "BeelineObject", 'Element', 'Server'],
            # usecols=["DATETIME_ID", "LAC", "CELL_ID", "CELL_NAME", "CDR", "CDR_Attempts", "CDR_Drops"],
            parse_dates=["DATETIME_ID"],
            dtype=datatype_dict
        ) for f in filelist)

    df100 = pd.concat(df_from_each_file, ignore_index=False)

    df100['DD'] = df100['DATETIME_ID'].dt.date
    del df100['DATETIME_ID']

    print(df100.head())

    # get last date dataframe:
    idx = df100.groupby(["LAC", "CELL_ID"])['DD'].transform(max) == df100['DD']
    df200 = df100[idx]
    del df100

    print('df200 last cell date:')
    print(df200.head())

    agglist = {'CDR': ['count', 'mean'], 'CDR_Attempts': 'sum', 'CDR_Drops': 'sum'}
    df400 = df200.groupby(["LAC", "CELL_ID", "CELL_NAME", "BeelineObject", 'Element', 'Server', 'DD']).agg(agglist)

    del df200

    print('df400 Groupping:')
    # print(df400.describe())
    df400.to_csv("test_er_3g_15min", sep='\t')

if __name__ == '__main__':
    main()
