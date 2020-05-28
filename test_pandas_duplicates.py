import pandas as pd
import glob


file_path = 'Green_log_test/dr2*.csv_3g'
filelist = glob.glob(file_path)

df_from_each_file = (
    pd.read_csv(
        f,
        delimiter=';',
        decimal='.',
        header=0,
        # index_col=["LAC", "CELL_ID"],
        parse_dates=["DATETIME_ID", "DATETIME_SVR"],
        # dtype=datatype_dict
    ) for f in filelist)

df = pd.concat(df_from_each_file, ignore_index=False)

# df2 = df.reset_index().drop_duplicates(subset=["LAC", "CELL_ID", "DATETIME_SVR"], keep='first')\
# #     .set_index(["LAC", "CELL_ID"])

df['combined_id'] = pd.factorize(df["LAC"]+df["CELL_ID"])[0]

print(df.head(50))
# print(df.shape)
# print(df2.shape)


