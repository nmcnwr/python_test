import pandas as pd
import glob
import os
import sys

"""usage: 
    python3 oper_er_3g_15min.py server server2 interval 1
    python3 oper_er_3g_15min.py server server2 interval 6
    python3 oper_er_3g_15min.py server server2 interval 96 # for daily stat

"""
parse_dates = ['DATETIME_SVR', 'DATETIME_ID']

server = sys.argv[2] if len(sys.argv) >= 3 else 'server1'
interval = int(sys.argv[4]) if len(sys.argv) >= 5 else 96

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

    tablename = "oper_er_4g_" + server + '_' + interval_name.lower()
    storage = 'temp/oper_er_4g_' + server + '_' + interval_name + '.csv'
    file_path = "Green_log/er_4g_15min/" + dwhdb_conn + "/*.res"
    print(file_path)

    datatype_dict = {'TAC': 'uint16'
                     # ,
                     #              'E_CunSR_Attempts': 'uint16',
                     #              'E_CunSR_Drops': 'uint16',
                     #              'E_CunSSR_Attempts': 'uint16',
                     #              'E_CunSSR_Drops': 'uint16',
                     #              'E_RAB_DR_Attempts': 'uint16',
                     #              'E_RAB_DR_Drops': 'uint16',
                     #              'E_RAB_Setup_FR_Attempts': 'uint16',
                     #              'E_RAB_Setup_FR_Drops': 'uint16',
                     #              'E_RRC_Setup_FR_Attempts': 'uint16',
                     #              'E_RRC_Setup_FR_Drops': 'uint16',
                     #              'S1_Setup_FR_Attempts': 'uint16',
                     #              'S1_Setup_FR_Drops': 'uint16'
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
            index_col=["TAC", "CELL_NAME", "BEELINEOBJECT", 'ELEMENT', 'Server'],
            parse_dates=["DATETIME_ID"],
            dtype=datatype_dict
        ) for f in filelist)

    df100 = pd.concat(df_from_each_file, ignore_index=False)

    df100['DD'] = df100['DATETIME_ID'].dt.date
    del df100['DATETIME_ID']

    # print(df100.head())

    # get last date dataframe:
    idx = df100.groupby(["TAC", "CELL_NAME"])['DD'].transform(max) == df100['DD']
    df200 = df100[idx]
    del df100

    # print('df200 last cell date:')
    # print(df200.head())

    agglist = {
        'DD': ['count'],
        'E_CunSR': 'mean',
        'E_CunSR_Attempts': 'sum',
        'E_CunSR_Drops': 'sum',
        'E_CunSSR': 'mean',
        'E_CunSSR_Attempts': 'sum',
        'E_CunSSR_Drops': 'sum',
        'E_RAB_DR': 'mean',
        'E_RAB_DR_Attempts': 'sum',
        'E_RAB_DR_Drops': 'sum',
        'E_RAB_Setup_FR': 'mean',
        'E_RAB_Setup_FR_Attempts': 'sum',
        'E_RAB_Setup_FR_Drops': 'sum',
        'E_RRC_Setup_FR': 'mean',
        'E_RRC_Setup_FR_Attempts': 'sum',
        'E_RRC_Setup_FR_Drops': 'sum',
        'S1_Setup_FR': 'mean',
        'S1_Setup_FR_Attempts': 'sum',
        'S1_Setup_FR_Drops': 'sum',
    }
    df400 = df200.groupby(["TAC", "CELL_NAME", "BEELINEOBJECT", 'ELEMENT', 'Server', 'DD']).agg(agglist)

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
    from sqlalchemy.types import Date, Numeric  # String, DateTime

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

    df401.to_sql(tablename, engine, if_exists='replace', index=False, dtype=dtyp)
    df401_counter = len(df401.index)
    del df401

    print('update Oracle log table')

    import datetime
    dt_now = datetime.datetime.now()
    dict_ = {'ADAM_TABLENAME': tablename, 'RAW_QTY': df401_counter, 'DT': dt_now}
    df = pd.DataFrame([dict_])
    dtyp = {'ADAM_TABLENAME': types.VARCHAR(50), "RAW_QTY": Numeric, 'DT': types.DateTime}
    df.to_sql('oper_log_2', engine, if_exists='append', index=False, dtype=dtyp)


if __name__ == '__main__':
    main()
