import mysql.connector
import boto3
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

queryLicenses=os.environ["QUERY_LICENSES"]
queryMedias=os.environ["QUERY_MEDIAS"]
queryClubs=os.environ["QUERY_CLUBS"]
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
        ssl_ca='/certs/global-bundle.pem',buffered=True
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
        cur = conn.cursor(buffered=True)
        cur.execute(queryLicenses)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data1 = pd.DataFrame(rows, columns=columns)
   
        cur.execute(queryMedias)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data2 = pd.DataFrame(rows, columns=columns)
       

        cur.execute(queryClubs)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data3 = pd.DataFrame(rows, columns=columns)
        cur.close()
        CloseCon(conn)
        return data1,data2,data3



