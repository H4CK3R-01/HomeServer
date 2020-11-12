import mysql.connector


def execute_sql(sql):
    mydb = mysql.connector.connect(
        host="192.168.178.55",
        user="root",
        passwd="Admin!123",
        database="mydb"
    )
    cursor = mydb.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def prepare_sql(sql, params):
    mydb = mysql.connector.connect(
        host="192.168.178.55",
        user="root",
        passwd="Admin!123",
        database="mydb"
    )
    cursor = mydb.cursor(prepared=True)
    cursor.execute(sql, params)
    mydb.commit()
    try:
        return cursor.lastrowid
    except AttributeError:
        return
