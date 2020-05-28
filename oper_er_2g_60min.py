import pandas as pd
import glob
import os
import sys
import time
import datetime

"""usage: 
    python3 oper_er_2g_60min.py server server2 interval 1
    python3 oper_er_2g_60min.py server server2 interval 6
    python3 oper_er_2g_60min.py server server2 interval 96 # for daily stat

"""
parse_dates = ['DATETIME_SVR', 'DATETIME_ID']

server = sys.argv[2] if len(sys.argv) >= 3 else 'server1'
interval = int(sys.argv[4]) if len(sys.argv) >= 5 else 5

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

    tablename = "oper_er_2g_" + server + '_60' + interval_name.lower()
    storage = 'temp/oper_er_2g_' + server + '_60' + interval_name + '.csv'
    file_path = "Green_log/er_2g_60min/" + dwhdb_conn + "/*.res"
    print(file_path)

    datatype_dict = {'LAC': 'str', 'CELL_NAME': 'str', 'BAND': 'uint16', 'PERIOD_DURATION': 'uint16'}

    filelist = glob.glob(file_path)
    filelist.sort(key=os.path.getmtime)
    filelist = filelist[-interval:]

    start = time.time()

    df_from_each_file = (
        pd.read_csv(
            f,
            delimiter=';',
            decimal='.',
            header=0,
            index_col=['Server', 'Element', 'PERIOD_DURATION', "LAC", "CELL_ID", "CELL_NAME", 'BAND', "SITE_NAME"],
            parse_dates=["DATETIME_ID", "DATETIME_SVR"],
            dtype=datatype_dict
        ) for f in filelist)

    df50 = pd.concat(df_from_each_file, ignore_index=False)

    # delete duplicates
    df100 = df50.reset_index().drop_duplicates(subset=["LAC", "CELL_ID", "CELL_NAME", "DATETIME_SVR"], keep='last') \
        .set_index(['Server', 'Element', 'PERIOD_DURATION', "LAC", "CELL_ID", "CELL_NAME", 'BAND', "SITE_NAME"])

    # fill zeros for KPI NaNs
    str_cols = df100.columns[df100.dtypes == 'float64']
    df100[str_cols] = df100[str_cols].fillna(0)
    df100.fillna(0, inplace=True)

    # fill zeros for KPI NaNs
    str_cols = df100.columns[df100.dtypes == 'uint16']
    df100[str_cols] = df100[str_cols].fillna(0)
    df100.fillna(0, inplace=True)

    # make date out of datetime
    df100['DD'] = df100['DATETIME_ID'].dt.normalize()
    df100['DT'] = df100['DATETIME_ID']

    df100['DDSVR'] = df100['DATETIME_SVR'].dt.normalize()
    df100['DTSVR'] = df100['DATETIME_SVR']

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

    df100 = df100.astype({"CDR": 'float16',
                          "CunSR": 'float16',
                          "CunSSR": 'float16',
                          "SDCDR": 'float16',
                          "TAFR": 'float16'
                          })

    # print(df100.head())

    # get indexes for last date dataframe:
    idx = df100.groupby(['Element', "LAC", "CELL_ID", "CELL_NAME"])['DD'].transform(max) == df100['DD']
    df200 = df100[idx]
    del df100

    # create slices for KPI AZ(Above Zero) and AT(Above Threshold)
    df200['CDR_Drops_AZ'] = (df200.CDR_Drops > 0).map({True: 1, False: 0})
    df200['CDR_Drops_AT'] = ((df200.CDR_Drops > 0) & (df200.CDR > 1.15)).map({True: 1, False: 0})

    df200['CunSR_Drops_AZ'] = (df200.CunSR_Drops > 0).map({True: 1, False: 0})
    df200['CunSR_Drops_AT'] = ((df200.CunSR_Drops > 0) & (df200.CunSR > 5)).map({True: 1, False: 0})

    df200['CunSSR_Drops_AZ'] = (df200.CunSSR_Drops > 0).map({True: 1, False: 0})
    df200['CunSSR_Drops_AT'] = ((df200.CunSSR_Drops > 0) & (df200.CunSSR > 2.5)).map({True: 1, False: 0})

    df200['SDCDR_Drops_AZ'] = (df200.SDCDR_Drops > 0).map({True: 1, False: 0})
    df200['SDCDR_Drops_AT'] = ((df200.SDCDR_Drops > 0) & (df200.SDCDR > 1.5)).map({True: 1, False: 0})

    df200['TAFR_Drops_AZ'] = (df200.TAFR_Drops > 0).map({True: 1, False: 0})
    df200['TAFR_Drops_AT'] = ((df200.TAFR_Drops > 0) & (df200.TAFR > 2.5)).map({True: 1, False: 0})

    agglist = {
        'DD': ['count'],
        'DT': ['min', 'max'],
        'DTSVR': ['max'],
        'DDSVR': ['max'],
        'CDR': 'mean',
        'CDR_Attempts': 'sum',
        'CDR_Drops': ['sum'],
        'CDR_Drops_AZ': 'sum',
        'CDR_Drops_AT': 'sum',
        'CunSR': 'mean',
        'CunSR_Attempts': 'sum',
        'CunSR_Drops': ['sum'],
        'CunSR_Drops_AZ': 'sum',
        'CunSR_Drops_AT': 'sum',
        'CunSSR': 'mean',
        'CunSSR_Attempts': 'sum',
        'CunSSR_Drops': ['sum'],
        'CunSSR_Drops_AZ': 'sum',
        'CunSSR_Drops_AT': 'sum',
        'SDCDR': 'mean',
        'SDCDR_Attempts': 'sum',
        'SDCDR_Drops': ['sum'],
        'SDCDR_Drops_AZ': 'sum',
        'SDCDR_Drops_AT': 'sum',
        'TAFR': 'mean',
        'TAFR_Attempts': 'sum',
        'TAFR_Drops': ['sum'],
        'TAFR_Drops_AZ': 'sum',
        'TAFR_Drops_AT': 'sum',
    }

    df400 = df200.groupby(['Server', 'Element', 'PERIOD_DURATION', "LAC", "CELL_ID", "CELL_NAME", 'BAND', "SITE_NAME",
                           'DD']).agg(agglist)
    del df200

    end = time.time()
    print('DataFrame counting time:', end=' ')
    print(end-start)

    # put all columns levels to one level
    df400.columns = ['_'.join(col) for col in df400.columns]
    dtsvr = df400['DTSVR_max'].max()
    # ddsvr = df400['DDSVR_max'].max()

    print('df400 saving to file...', storage)

    df400['CDR_mean'] = df400['CDR_mean'].astype(float).round(2)
    df400['CunSR_mean'] = df400['CunSR_mean'].astype(float).round(2)
    df400['CunSSR_mean'] = df400['CunSSR_mean'].astype(float).round(2)
    df400['SDCDR_mean'] = df400['SDCDR_mean'].astype(float).round(2)
    df400['TAFR_mean'] = df400['TAFR_mean'].astype(float).round(2)

    df400.reset_index().to_csv(storage, index=False, header=True, decimal=',', sep='\t', float_format='%.1f')

    print('df400 saving to Oracle...', tablename)
    start_oracle = time.time()
    from sqlalchemy import create_engine
    from sqlalchemy import types
    from sqlalchemy.types import Date, Numeric  # ,String, DateTime

    # engine = create_engine('oracle://CC:CC@RAN_dcn')
    engine = create_engine('oracle://ADAM:ADAM@10.136.147.37:1521/ran')

    df400 = df400.reset_index(drop=False, inplace=False)
    df400.columns = map(lambda x: str(x).upper(), df400.columns)

    df401 = df400
    # set VARCHAR(50) type for all string objects
    dtyp = {c: types.VARCHAR(50)
            for c in df401.columns[df401.dtypes == 'object'].tolist()}

    dtyp["DD"] = Date
    # dtyp["CELL_NAME"] = types.VARCHAR(50)

    connection = engine.raw_connection()
    cursor = connection.cursor()
    cursor.callproc("PR_DROP_TABLE", [tablename])
    cursor.close()
    connection.commit()

    # OSS Server DateTime in oracle-varchar format
    dtsvr_raw = str(dtsvr)
    # ddsvr_raw = str(ddsvr)

    if interval == 1:
        df401.to_sql(tablename, engine, if_exists='append', index=False, dtype=dtyp)
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("PR_RAW_LOG_ROP", [tablename, dtsvr_raw])
            cursor.close()
            connection.commit()
        finally:
            connection.close()
    elif interval == 3:
        df401.to_sql(tablename, engine, if_exists='append', index=False, dtype=dtyp)
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("PR_RAW_LOG_ROP", [tablename, dtsvr_raw])
            cursor.close()
            connection.commit()
        finally:
            connection.close()
    elif interval == 96:
        df401.to_sql(tablename, engine, if_exists='append', index=False, dtype=dtyp)
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("PR_RAW_2G_DAY", [tablename])
            cursor.close()
            connection.commit()
        finally:
            connection.close()
    else:
        df401.to_sql(tablename, engine, if_exists='append', index=False, dtype=dtyp)

    con = engine.connect()
    sql = f"grant select on {tablename} to ran_ro"
    con.execute(sql)
    con.close()

    end_oracle = time.time()
    print('Oracle counting time:', end=' ')
    print(end_oracle-start_oracle)

    print('update Oracle log table')

    df401_counter = len(df401.index)

    dt_now = datetime.datetime.now()
    dict_ = {'ADAM_TABLENAME': tablename, 'DTSVR_START': dtsvr, 'RAW_QTY': df401_counter, 'DT': dt_now}
    df = pd.DataFrame([dict_])
    dtyp = {'ADAM_TABLENAME': types.VARCHAR(50), 'DTSVR_START': types.DateTime, "RAW_QTY": Numeric,
            'DT': types.DateTime}
    df.to_sql('oper_log_4', engine, if_exists='append', index=False, dtype=dtyp)


if __name__ == '__main__':
    main()
