import pandas as pd
import time
import timeit

f = 'temp/row_er_3g_utest.csv'

df = pd.read_csv(
    f,
    delimiter=';',
    decimal=',',
    header=0,
    index_col=["LAC", "CELL_ID"],
    parse_dates=["DTSVR_MAX"],

)
print(df.head(15))


agglist = {
        'CDR_DROPS_SUM': ['sum', ('intervals', lambda x: (x > 0).sum()), 'count']
    }

cols = ["LAC", "CELL_ID"]


print("Loop1", end='=')
start = time.time()
for i in range(2):
    df_agg10 = df.groupby(cols).agg(agglist)
    print(df_agg10)
end = time.time()

agglist = {

        'CDR_DROPS_SUM': ['sum', ('intervals', lambda x: x.ne(0).sum().astype(int)), 'count']
    }
print("Loop2", end='=')
start2 = time.time()
for i in range(2):
    gr = df.groupby(["CELL_ID"])
    df_agg10 = gr.agg(agglist)
    print(df_agg10)
end2 = time.time()

print(end - start)
print(end2 - start2)




