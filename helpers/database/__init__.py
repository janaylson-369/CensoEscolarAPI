from flask import g
from helpers.application import app
from helpers.enviroment import enviroment
import psycopg2


DB_CONFIGURACAO = {
    "host": enviroment.get("DB_HOST"),
    "port": int(enviroment.get("DB_PORT")),
    "database": enviroment.get("DB_NAME"),
    "user": enviroment.get("DB_USER"),
    "password": enviroment.get("DB_PASSWORD")
}

def get_connexao():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = psycopg2.connect(**DB_CONFIGURACAO)
    return conn

@app.teardown_appcontext
def close_db(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()

