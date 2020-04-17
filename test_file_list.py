
import glob
import os



file_path = "Green_log/er_3g_15min/dwhdb_MSK/*.res"

print('Start reading log files: filelist and lastfile')
filelist = glob.glob(file_path)
filelist.sort(key=os.path.getmtime)


newff = filelist[-5:-1]
print(newff)

