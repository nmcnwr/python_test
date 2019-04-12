import pymysql.cursors

# Подключиться к базе данных.
connection = pymysql.connect(host='172.26.142.174',
                             user='uric',
                             password='uio987',
                             db='nmcdb',
                             charset='cp1251',
                             cursorclass=pymysql.cursors.DictCursor)

print("connect successful!!")


mycursor = connection.cursor()

mycursor.execute("SELECT * FROM yes_no where id=1")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
