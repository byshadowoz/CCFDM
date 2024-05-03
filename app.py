from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error
import pandas as pd
import os

dataCSV = pd.read_csv('CCFDM/fraudtestdumed.csv')
columnas = dataCSV.columns.tolist()

def create_connection():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_file = os.path.join(dir_path, "bank.db")

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        raise e 

    return conn

def create_table(conn, columnas):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='creditcard'")
    if cur.fetchone() is None:
        try:
            sql = '''CREATE TABLE creditcard({})'''.format(', '.join(columnas))
            conn.execute(sql)
            conn.commit()
            print("Tabla 'creditcard' creada exitosamente.")
        except Error as e:
            print("Error al crear la tabla 'creditcard':", e)

def insert_datos(conn, info):
    try:
        cur = conn.cursor()
        columns = ', '.join(info.keys())
        placeholders = ', '.join('?' * len(info))
        sql = f"INSERT INTO creditcard ({columns}) VALUES ({placeholders})"
        cur.execute(sql, tuple(info.values()))
        conn.commit()
        print("Datos insertados exitosamente en la tabla 'creditcard'.")
    except Error as e:
        print("Error al insertar datos en la tabla 'creditcard':", e)

def check_database(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM creditcard")

    rows = cur.fetchall()

    for row in rows:
        print(row)


app = Flask(__name__)

@app.route('/datos', methods=['POST'])
def post_datos():
    info = request.get_json()
    conn = create_connection()
    create_table(conn,dataCSV.columns.tolist())
    insert_datos(conn, info)
    check_database(conn)
    return jsonify({'message': '¡Información guardada con éxito!'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5050)