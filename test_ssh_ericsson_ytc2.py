import paramiko

host = 'ytc2'
user = 'noac_spb'
secret = 'spb216'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Подключение
client.connect(hostname=host, username=user, password=secret, port=port)

stdin, stdout, stderr = client.exec_command("uname -a")
opt = stdout.readlines()
opt = "".join(opt)
print(opt)


remotefilepath=r"/home/noac_spb/cha/cmdfile/FILE1.txt"
localfilepath=r"C:\\\\Users\\\\pbkuznetsov\\\\PycharmProjects\\\\untitled_test1\\\\venv\\\\FILE1.txt"
#Downloading a file from remote machine

# ftp_client=client.open_sftp()
# ftp_client.get(remotefilepath,localfilepath)
# ftp_client.close()

#Uploading file from local to remote machine

ftp_client=client.open_sftp()
# get - ok !
#ftp_client.get(remotefilepath,localfilepath)

#put - ok
ftp_client.put(localfilepath,remotefilepath)
ftp_client.close()

client.close()