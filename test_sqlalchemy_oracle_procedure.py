
from sqlalchemy import create_engine

db = create_engine('oracle://ADAM:ADAM@Violet')
connection = db.raw_connection()

# parameterIn = 1
# parameterOut = "@parameterOut"
try:
    cursor = connection.cursor()
    # cursor.callproc("storedProcedure", [parameterIn, parameterOut])
    cursor.callproc("PR_RAW_LOG", ["table1", "2020.04.30 11:11:33"])
    # fetch result parameters
    # results = list(cursor.fetchall())
    cursor.close()
    connection.commit()
finally:
    connection.close()

