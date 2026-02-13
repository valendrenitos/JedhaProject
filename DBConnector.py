import mysql.connector
import boto3
from dotenv import load_dotenv
import os
load_dotenv()

queryLicenses=os.environ["QUERY_LICENSES"]
queryMedias=os.environ["QUERY_MEDIAS"]
conn = None

def CloseCon(conn):
    conn.close()

def TryConnect():
    try:
        conn = mysql.connector.connect(
            host=os.environ["DB_ADDRESS"],
            port=3306,
            database='mysql',
            user=os.environ["MYSQL_DB_USER"],
            password=os.environ["MYSQL_DB_PSWD"],
            ssl_disabled=False,
        ssl_ca='/certs/global-bundle.pem'
        )
        cur = conn.cursor()
        cur.execute('SELECT VERSION();')
        print(cur.fetchone()[0])
        cur.close()
        return conn
    except Exception as e:
        print(f"Database error: {e}")
        raise
   



def getData():
    conn=TryConnect()
    if conn:
        data1=conn._execute_query(queryLicenses)
        data2=conn._execute_query(queryMedias)
        CloseCon(conn)
        return data1,data2


conn=TryConnect()
CloseCon(conn)
