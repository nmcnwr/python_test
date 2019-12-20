

import os
import re
import glob
import paramiko
import cx_Oracle

import sys
import time


# {'MSC2xxxRNC55DHC': {'MSC': 'MSC2', 'RNC': 'RNC55DHC', 'FILE': 'YTC1_MSS_MGMAP.result', 'LAC': {'line 20': '250-99-12345', 'line 21': '250-99-12346'}}}
DictLAC = {}


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def main():

    #os.chdir("C:\\Web\\NMCPython\\logs")
    os.chdir("logs")
    #check working dir:
    print(os.getcwd())

    hostlist = ['YTC1','YTC2','YTC3','YTC4','YTC5','YTC6']


    user = 'noac_spb'
    secret = 'spb216'
    port = 22
    filename = "MSS_MGMAP.result"

    filelist = glob.glob('*MGMAP.result')
    # del old result files
    for filedelname in filelist:
        try:
            os.remove(filedelname)
        except:
            print("Error while deleting file : ", filedelname)

    # connect each server
    for host in hostlist:
        print(host,' ', end='')
        OSSConnection(host, user, secret, port, filename)

    print()

    # read files in log dir for parsing
    filelist = glob.glob('*MGMAP.result')
    for fileparsename in filelist:
        try:
            print('46')
            Parsefile(fileparsename)
        except:
            print("Error while getting file : ", fileparsename)

    connstr = 'CC/CC@10.136.147.37:1521/RAN'
    con = cx_Oracle.connect(connstr)
    cur = con.cursor()

    statement = 'truncate table ERICSSON_MSS_MGMAP_PY'
    cur.execute(statement)

    spinner = spinning_cursor() # get spinlist


    with open('out_MGMAP.txt', 'w') as f:
        print('Filename:', filename, file=f)
        for key1 in DictLAC:
            print('', file=f)
            #print(key1, file=f)

            for LineNUM, LAC in DictLAC[key1]['LAC'].items():
                print('MSC=', DictLAC[key1]['MSC'], end='', file=f)
                print(' RNC=', DictLAC[key1]['RNC'], end='', file=f)
                print(' FILE=', DictLAC[key1]['FILE'], end='', file=f)
                print(' linenum=', LineNUM, LAC, file=f)

                # 250-99-11003 - needed the last part
                splitLAC = LAC.split("-")
                LAC = splitLAC[2]


                sys.stdout.write(next(spinner)) # spin start
                sys.stdout.flush()              # spin start




                rows = [(DictLAC[key1]['FILE'], LineNUM, DictLAC[key1]['MSC'], DictLAC[key1]['RNC'], LAC)]
                cur.bindarraysize = 1
                cur.setinputsizes(64, int, 16, 16, 16)
                cur.executemany("insert into ERICSSON_MSS_MGMAP_PY(FILENAME, LINEINFILE, NE, RNCNAME, LAC) values (:1, :2, :3, :4, :5)", rows)
                con.commit()

                sys.stdout.write('\b')          # spin del


    cur.close()
    con.close()

def Parsefile(file):

    fh = open(file)
    print('Parsefile:', file)

    for line_no, line in enumerate(fh):

        NE_search = re.search('^NE=(\w+)', line, re.IGNORECASE)

        if NE_search:
            NE = NE_search.group(1)
            print(NE)

        RNC_search = re.search('^<MGMAP:RNC=(.*);$', line)

        if RNC_search:
            RNC = RNC_search.group(1)
            key1 = NE + 'xxx' + RNC

            DictLAC[key1] = {'MSC': NE, 'RNC': RNC, 'FILE': file}
            DictLAC[key1]['LAC'] = {}
            #print(NE,RNC)

        LAI_search = re.search('(250-99-\d+)$', line)

        if LAI_search:
            LAI = LAI_search.group(1)
            line_no = line_no + 1
            print('107:', file, line_no, NE, RNC, LAI)

            #{'MSC2xxxRNC55DHC': {'MSC': 'MSC2', 'RNC': 'RNC55DHC', 'SERVER': 'YTC1', 'FILE': 'test.exe', 'LAC': {'line 20': '250-99-12345', 'line 21': '250-99-12346'}}}


            DictLAC[key1]['LAC'][line_no] = LAI


            #!# print(DictLAC)


    fh.close()


def OSSConnection(host, user, secret, port, filename):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Подключение
    client.connect(hostname=host, username=user, password=secret, port=port)

    remotefilepath = "/home/noac_spb/cha/response/" + filename
    windows_path = ''       # r"logs\\"
    filename = host+"_"+filename
    localfilepath = windows_path + filename

    # Downloading a file from remote machine

    ftp_client = client.open_sftp()
    ftp_client.get(remotefilepath, localfilepath)
    ftp_client.close()

    client.close()



# todo: open file filename
# todo: parse file and put data to the tuple or dictionary
# todo: connect Oracle/mysql
# todo: put dictionary to Oracle/mysql

if __name__ == '__main__':
   main()

