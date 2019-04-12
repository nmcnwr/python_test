from ftplib import FTP

ftp = FTP('10.136.147.142')
ftp.login('udata','DataU')
data = ftp.retrlines('LIST')

print(data)