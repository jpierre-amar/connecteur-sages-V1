import pyodbc
import psycopg2
import json
import os

CREDENTIALS_FILE = "app/services/credentials.json"

def connect_to_sqlserver(server, user, password, database):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("Erreur de connexion :", e)
        return None


def connect_to_postgres(host, user, password, database, port="5432"):
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=database,
            user=user,
            password=password,
            port=port
        )
        print("✅ Connexion PostgreSQL réussie")
        return conn
    except Exception as e:
        print("❌ Erreur PostgreSQL :", e)
        return None
    
    
def save_credentials(data):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    with open(CREDENTIALS_FILE, "r") as f:
        return json.load(f)