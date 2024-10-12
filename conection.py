import psycopg2

def connection_database():
    connection = psycopg2.connect(
        database="lessondb",
        user="postgres",
        host="localhost",
        password="1234",
        port=5432
    )
    return connection

def close_con(conn,cur):
    conn.close()
    cur.close()