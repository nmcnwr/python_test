import pandas as pd
import glob
import os
import sys

"""usage: 
    python3 oper_er_2g_15min.py server server2 interval 1
    python3 oper_er_2g_15min.py server server2 interval 6
    python3 oper_er_2g_15min.py server server2 interval 96 # for daily stat

"""
parse_dates = ['DATETIME_SVR', 'DATETIME_ID']

server = sys.argv[2] if len(sys.argv) >= 3 else 'server1'
interval = int(sys.argv[4]) if len(sys.argv) >= 5 else 1

interval_name = 'rop' + str(interval)
if server == 'server1':
    dwhdb_conn = 'dwhdb_MSK'
elif server == 'server2':
    dwhdb_conn = 'dwhdb_yaroslavl'
else:
    print('Server not defined. Usage: <scriptname> server server1')
    quit()


def main():
    engine1()


def engine1():
    """
     Take all file from file_path to DF
     Take last date DD
     Aggregate Objects and KPI with mean, sum
     Save to csv (storage)
     Save to Oracle tablename

     """
    print('dwhdb_conn=', dwhdb_conn, ', server=', server, ', interval=', interval)

    tablename = "oper_er_2g_" + server + '_' + interval_name.lower()
    storage = 'temp/oper_er_2g_' + server + '_' + interval_name + '.csv'
    file_path = "Green_log/er_2g_15min/" + dwhdb_conn + "/*.res"
    print(file_path)

    datatype_dict = {'LAC': 'str',
                     'CELL_NAME': 'str',
                     'BAND': 'uint16',
                     'PERIOD_DURATION': 'uint16'

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
            index_col=["LAC", "CELL_NAME", "SITE_NAME", 'Element', 'Server', 'BAND', 'PERIOD_DURATION'],
            parse_dates=["DATETIME_ID"],
            dtype=datatype_dict
        ) for f in filelist)

    df100 = pd.concat(df_from_each_file, ignore_index=False)

    df100 = df100[(df100['CDR'].notnull()) & (df100['CDR_Attempts'].notnull())]
    df100['DD'] = df100['DATETIME_ID'].dt.date
    del df100['DATETIME_ID']

    # print(df100.head())

    # get last date dataframe:
    idx = df100.groupby(["LAC", "CELL_NAME"])['DD'].transform(max) == df100['DD']
    df200 = df100[idx]
    del df100

    # print('df200 last cell date:')
    # print(df200.head())

    agglist = {
        'DD': ['count'],
        'CDR': 'mean',
        'CDR_Attempts': 'sum',
        'CDR_Drops': 'sum',
        'CunSR': 'mean',
        'CunSR_Attempts': 'sum',
        'CunSR_Drops': 'sum',
        'CunSSR': 'mean',
        'CunSSR_Attempts': 'sum',
        'CunSSR_Drops': 'sum',
        'SDCDR': 'mean',
        'SDCDR_Attempts': 'sum',
        'SDCDR_Drops': 'sum',
        'TAFR': 'mean',
        'TAFR_Attempts': 'sum',
        'TAFR_Drops': 'sum'
    }
    df400 = df200.groupby(["LAC", "CELL_NAME", "SITE_NAME", 'Element', 'Server', 'BAND', 'PERIOD_DURATION', 'DD'])\
        .agg(agglist)

    # put all columns levels to one level
    df400.columns = ['_'.join(col) for col in df400.columns]

    del df200

    print('df400 saving...')
    print('df400 to file...', storage)

    df400 = df400.round(decimals=2)
    df400.reset_index().to_csv(storage, index=False, header=True, decimal=',', sep='\t', float_format='%.1f')

    print('df400 to Oracle...', tablename)
    from sqlalchemy import create_engine
    from sqlalchemy import types
    from sqlalchemy.types import Date, Numeric   # ,String, DateTime

    # engine = create_engine('oracle://CC:CC@RAN_dcn')
    engine = create_engine('oracle://ADAM:ADAM@10.136.147.37:1521/ran')

    df400 = df400.reset_index(drop=False, inplace=False)
    df400.columns = map(lambda x: str(x).upper(), df400.columns)
    # print(df400.info())

    df401 = df400
    # set VARCHAR(50) type for all string objects
    dtyp = {c: types.VARCHAR(50)
            for c in df401.columns[df401.dtypes == 'object'].tolist()}

    # set Date type for DD
    del dtyp["DD"]
    dtyp["DD"] = Date

    dtyp["CELL_NAME"] = types.VARCHAR(50)

    df401.to_sql(tablename, engine, if_exists='replace', index=False, dtype=dtyp)
    df401_counter = len(df401.index)
    del df401

    con = engine.connect()
    sql = f"grant select on {tablename} to ran_ro"
    con.execute(sql)
    con.close()

    print('update Oracle log table')

    import datetime
    dt_now = datetime.datetime.now()
    dict_ = {'ADAM_TABLENAME': tablename, 'RAW_QTY': df401_counter, 'DT': dt_now}
    df = pd.DataFrame([dict_])
    dtyp = {'ADAM_TABLENAME': types.VARCHAR(50), "RAW_QTY": Numeric, 'DT': types.DateTime}
    df.to_sql('oper_log_2', engine, if_exists='append', index=False, dtype=dtyp)


if __name__ == '__main__':
    main()
