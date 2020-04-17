import pandas as pd
import glob
import os
import re

parse_dates = ['DATETIME_SVR']


def main():

    kpilist = ('CDR', 'CunSR')
    # kpilist = ('CDR', 'CunSR', 'CunSSR', 'RAB_DR_PS', 'RAB_FR_PS', 'RAB_Setup_FR_CS', 'RRC_CSetup_FR_CS',
    #            'RRC_CSetup_FR_PS', 'U_CunSR_PS', 'U_CunSSR_PS')
    for kpiname in kpilist:
        engine1(kpiname)


def engine1(kpi_name):

    kpiname1 = kpi_name + '_Drops'
    kpiname2 = kpi_name + '_Attempts'

    kpi1_value_threshold = 0

    avg_kpiname1 = 'avg_' + kpiname1
    avg_kpiname2 = 'avg_' + kpiname2

    file_path = "Green_log/er_3g_15min/dwhdb_MSK/*.res"
    datatype_dict = {'LAC': 'uint16', 'CELL_ID': 'uint16', kpiname1: 'uint16', kpiname2: 'uint16'}

    # todo: kpi_dict{'CDR_DROPS':10}
    # todo: write log to file .txt or .xls
    # done: loop for 2 KPIs

    #############
    #
    # Get list of files and devide filelist to filelist(except lastfile) and lastfile

    print('Start reading log files: filelist and lastfile')
    filelist = glob.glob(file_path)
    filelist.sort(key=os.path.getmtime)

    lastfile = filelist[-1]
    del filelist[-1]

    print('filelist:', filelist[0], ' - ', filelist[-1], '\nlastfile:', lastfile)
    # statement = "kpistat_5csv\dwhdb_MSK_202003241000_er_3g_15min.res"

    m = re.match(".*_(\d{4})(\d{2})(\d{2})(\d{4})_.*", filelist[0])
    if m:
        period1_start = m.group(1) + '-' + m.group(2) + '-' + m.group(3) + ' ' + m.group(4)

    m = re.match(".*_(\d{4})(\d{2})(\d{2})(\d{4})_.*", filelist[-1])
    if m:
        period1_stop = m.group(1) + '-' + m.group(2) + '-' + m.group(3) + ' ' + m.group(4)

    print('filelist periods:', period1_start, ' - ', period1_stop)

    m = re.match(".*_(\d{4})(\d{2})(\d{2})(\d{4})_.*", lastfile)
    if m:
        period_lastfile = m.group(1) + '-' + m.group(2) + '-' + m.group(3) + ' ' + m.group(4)
        print('lastfile period:', period_lastfile)


    ###########
    #
    # Part 1. Read filelist

    print('Start read_csv from filelist')
    # filelist = glob.glob(os.path.join(path, "dwhdb_yaroslavl_202003*_er_3g_15min.res"))
    # advisable to use os.path.join as this makes concatenation OS independent

    df_from_each_file = (
            pd.read_csv(
                    f,
                    delimiter=';',
                    decimal='.',
                    header=0,
                    index_col=["LAC", "CELL_ID"],
                    usecols=["DATETIME_SVR", "LAC", "CELL_ID", kpiname1, kpiname2],
                    parse_dates=["DATETIME_SVR"],
                    dtype=datatype_dict
            ) for f in filelist)


    df100 = pd.concat(df_from_each_file, ignore_index=False)
    # print(df100.head(5))

    print('Start pivot table from filelist')

    # df130 = df100.query('LAC == 27664')
    # del df100

    df131 = pd.pivot_table(df100
                            , index=['LAC', 'CELL_ID']
                            # , columns=['DATETIME_SVR']
                            , values=[kpiname1, kpiname2]
                            , aggfunc={kpiname1: 'mean', kpiname2: 'mean'}
                           )
    # print(df131.head(5))

    # round aggregated kpinames 1&2:
    round_decimal = 1
    df131[kpiname1] = df131[kpiname1].apply(lambda x: round(x, round_decimal))
    df131[kpiname2] = df131[kpiname2].apply(lambda x: round(x, round_decimal))

    df131 = df131.rename({kpiname1: avg_kpiname1, kpiname2: avg_kpiname2}, axis='columns')
    # print(df131.head(5))
    del df100

    ###########
    #
    # Part 2. Read the last csv file - lastfile
    print('Start reading last file (to compare with)')

    df200 = pd.read_csv(
            # os.path.join(path, "dwhdb_yaroslavl_202003191400_er_3g_15min.csv"),
            lastfile,
            delimiter=';',
            decimal='.',
            header=0,
            index_col=["LAC", "CELL_ID"],
            usecols=["LAC", "CELL_ID", kpiname1, kpiname2],
            dtype=datatype_dict
        )
    # print(df200.head(5))

    ###########
    #
    # Part 3. Join, merge dataframes
    print('Start merge average KPI and last KPI')

    df300 = pd.merge(df131, df200, left_index=True, right_index=True)
    # print(df300.head(5))
    del df131
    del df200

    # df310 = df300[(df300.CDR_Drops > 8)]
    df305 = df300.rename({kpiname1: 'KPI1', kpiname2: 'KPI2'}, axis='columns')

    df310 = df305.query('KPI1 > @kpi1_value_threshold' and 'CELL_ID == 43593')
    df315 = df310.rename({'KPI1': kpiname1, 'KPI2': kpiname2}, axis='columns')
    print(df315.head())

    print(df315.describe())

    del df300


if __name__ == '__main__':
    main()
