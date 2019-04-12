
import paramiko

host = '10.136.147.142'
user = 'udata'
secret = 'DataU'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Подключение
client.connect(hostname=host, username=user, password=secret, port=port)

stdin, stdout, stderr = client.exec_command("uname -a")
opt = stdout.readlines()
opt = "".join(opt)
print(opt)


client.close()

