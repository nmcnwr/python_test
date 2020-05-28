import pandas as pd
import glob
import os
import time
import numpy as np
import sys


parse_dates = ['DATETIME_SVR', 'DATETIME_ID']

server = 'server1'
interval = 6
#  dwhdb_conn = 'compare_MSK'
dwhdb_conn = 'dwhdb_MSK'
interval_name = 'rop' + str(interval)


def main():
    engine1()


def engine1():

    storage = 'temp/oper_er_2g_' + server + '_' + interval_name + '.csv'
    file_path = "Green_log/er_2g_15min/" + dwhdb_conn + "/*.res"
    print(file_path)

    datatype_dict = {'LAC': 'str', 'CELL_NAME': 'str', 'BAND': 'uint16'
                     , 'PERIOD_DURATION': 'uint16'

                     }

    filelist = glob.glob(file_path)
    filelist.sort(key=os.path.getmtime)
    filelist = filelist[-interval:]

    df_from_each_file = (
        pd.read_csv(
            f,
            delimiter=';',
            decimal='.',
            header=0,

            index_col=['Server', 'Element', 'PERIOD_DURATION', "SITE_NAME", 'BAND',   "LAC", "CELL_NAME"],
            parse_dates=["DATETIME_ID", "DATETIME_SVR"],
            dtype=datatype_dict
        ) for f in filelist)

    df100 = pd.concat(df_from_each_file, ignore_index=False)

    df100 = df100[(df100['CDR'].notnull()) & (df100['CDR_Attempts'].notnull())]
    df100['DD'] = df100['DATETIME_ID'].dt.normalize()
    # df100['DD'] = pd.to_datetime(df100['DD']).astype(np.int64)   # !!!

    df100['DT'] = df100['DATETIME_ID']
    df100['DTSVR'] = df100['DATETIME_SVR']

    # df100 = df100.astype({'DD': 'int32'})

    df100 = df100.astype({"CDR_Attempts": 'int16',
                          "CDR_Drops": 'int16',
                          "CunSR_Attempts": 'int16',
                          "CunSR_Drops": 'int16',
                          "CunSSR_Attempts": 'int16',
                          "CunSSR_Drops": 'int16',
                          "SDCDR_Attempts": 'int16',
                          "SDCDR_Drops": 'int16',
                          "TAFR_Attempts": 'int16',
                          "TAFR_Drops": 'int16'
                          })

    # df100 = df100.astype({"Element": 'category',
    #                       "Server": 'category',
    #                       "BAND": 'category',
    #                       "SITE_NAME": 'category',
    #                       "PERIOD_DURATION": 'category'
    #                       })

    df100 = df100.astype({"CDR": 'float16',
                          "CunSR": 'float16',
                          "CunSSR": 'float16',
                          "SDCDR": 'float16',
                          "TAFR": 'float16'
                          })

    print("generator")
    #  print(df100.memory_usage(deep=True))
    #  print(df100.dtypes)
    start2 = time.time()

    # get last date dataframe:
    idx = df100.groupby(["LAC", "CELL_NAME"])['DD'].transform(max) == df100['DD']
    df200 = df100[idx]

    print(df200.head())

    agglist = {
        'DD': ['count'],
        'DT': ['min', 'max'],
        'DTSVR': ['max'],
        'CDR': 'mean',
        'CDR_Attempts': 'sum',
        # 'CDR_Drops': ['sum', ('rop', lambda x: x.ne(0).sum().astype(int))]
        'CDR_Drops': ['sum', 'nunique']

    }

    df400 = df200.groupby(["LAC", "CELL_NAME"]).agg(agglist)

    print(df400.head(20))

    end2 = time.time()
    print(end2 - start2)

    # # put all columns levels to one level
    # df400.columns = ['_'.join(col) for col in df400.columns]
    # df400 = df400.round(decimals=2)
    # df400.reset_index().to_csv(storage, index=False, header=True, decimal=',', sep='\t', float_format='%.1f')


if __name__ == '__main__':
    main()
