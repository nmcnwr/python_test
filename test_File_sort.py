import glob
import os

files = glob.glob("kpistat_5csv/*.res")
files.sort(key=os.path.getmtime)
print('all files:')
print("\n".join(files))


last_file = files[-1]
del files[-1]
print('\nold files:')
print("\n".join(files))

print('\nlast file:')
print(last_file)

