import pandas as pd
import glob
import os

parse_dates = ['DATETIME_SVR', 'DATETIME_ID']


def main():
    engine1()


def engine1():
    """ testing """

    tablename = "oper_er_3g_15min_dwhdb_MSK".lower()
    storage = 'temp/oper_er_3g_15min_dwhdb_MSK.csv'
    file_path = "Green_log/er_3g_15min/dwhdb_MSK/*.res"

    datatype_dict = {'LAC': 'uint16', 'CELL_ID': 'uint16',
                     'CDR_Attempts': 'uint16',
                     'CDR_Drops': 'uint16',
                     'CunSR_Attempts': 'uint16',
                     'CunSR_Drops': 'uint16',
                     'CunSSR_Attempts': 'uint16',
                     'CunSSR_Drops': 'uint16',
                     'RAB_DR_PS_Attempts': 'uint16',
                     'RAB_DR_PS_Drops': 'uint16',
                     'RAB_FR_PS_Attempts': 'uint16',
                     'RAB_FR_PS_Drops': 'uint16',
                     'RAB_Setup_FR_CS_Attempts': 'uint16',
                     'RAB_Setup_FR_CS_Drops': 'uint16',
                     'RRC_CSetup_FR_CS_Attempts': 'uint16',
                     'RRC_CSetup_FR_CS_Drops': 'uint16',
                     'RRC_CSetup_FR_PS_Attempts': 'uint16',
                     'RRC_CSetup_FR_PS_Drops': 'uint16',
                     'U_CunSR_PS_Attempts': 'uint16',
                     'U_CunSR_PS_Drops': 'uint16',
                     'U_CunSSR_PS_Attempts': 'uint16',
                     'U_CunSSR_PS_Drops': 'uint16'
                     }

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
        'RAB_DR_PS': 'mean',
        'RAB_DR_PS_Attempts': 'sum',
        'RAB_DR_PS_Drops': 'sum',
        'RAB_FR_PS': 'mean',
        'RAB_FR_PS_Attempts': 'sum',
        'RAB_FR_PS_Drops': 'sum',
        'RAB_Setup_FR_CS': 'mean',
        'RAB_Setup_FR_CS_Attempts': 'sum',
        'RAB_Setup_FR_CS_Drops': 'sum',
        'RRC_CSetup_FR_CS': 'mean',
        'RRC_CSetup_FR_CS_Attempts': 'sum',
        'RRC_CSetup_FR_CS_Drops': 'sum',
        'RRC_CSetup_FR_PS': 'mean',
        'RRC_CSetup_FR_PS_Attempts': 'sum',
        'RRC_CSetup_FR_PS_Drops': 'sum',
        'U_CunSR_PS': 'mean',
        'U_CunSR_PS_Attempts': 'sum',
        'U_CunSR_PS_Drops': 'sum',
        'U_CunSSR_PS': 'mean',
        'U_CunSSR_PS_Attempts': 'sum',
        'U_CunSSR_PS_Drops': 'sum'
    }
    df400 = df200.groupby(["LAC", "CELL_ID", "CELL_NAME", "BeelineObject", 'Element', 'Server', 'DD']).agg(agglist)

    # put all columns levels to one level
    df400.columns = ['_'.join(col) for col in df400.columns]

    del df200

    print('df400 saving...')
    print('df400 to file...')

    df400 = df400.round(decimals=2)
    df400.reset_index().to_csv(storage, index=False, header=True, decimal=',', sep='\t', float_format='%.1f')

    print('df400 to Oracle...')
    from sqlalchemy import create_engine
    from sqlalchemy import types
    from sqlalchemy.types import Date  # String, DateTime

    engine = create_engine('oracle://CC:CC@RAN_dcn')

    # con = engine.connect()
    # con.execute("TRUNCATE TABLE CC.SERVER2_ER_3G_15MIN")

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

    # con.close()


if __name__ == '__main__':
    main()
