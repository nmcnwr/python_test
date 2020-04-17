import pandas as pd



df1 = pd.DataFrame(
    {
        "2020-03-01": [5, 3, 6, 4],
        "2020-03-02": [11, 3, 7, 3],
        "2020-03-03": [4, 3, 8, 5],
        "2020-03-04": [3, 3, 9, 8]
     }
)

df2 = df1.diff(axis=1, periods=1)

maxValuesObj = df1.max(axis=1)
print('Maximum value in each row : ')
print(maxValuesObj)



# get the column name of max values in every row
maxValueIndexObj = df1.idxmax(axis=1)

print("Max values of row are at following columns :")
print(maxValueIndexObj)


print(df1)
print(df2)


