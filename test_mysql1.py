import mysql.connector

mydb = mysql.connector.connect(
  host="172.26.142.172",
  user="uric",
  passwd="uio987",
  database="nmcdb"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM yes_no where id=1")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

