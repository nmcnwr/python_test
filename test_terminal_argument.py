import sys

server = sys.argv[2] if len(sys.argv) >= 3 else 'server1'

if server == 'server1':
    dwhdb_conn = 'dwhdb_MSK'
elif server == 'server2':
    dwhdb_conn = 'dwhdb_yaroslavl'
else:
    print('Server not defined. Usage: <scriptname> server server1')
    quit()

table = 'oper_'+dwhdb_conn+'_tt'
print(table)
