from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error

# Función para crear una conexión a la base de datos SQLite
def create_connection(db_file):
    conn = None;
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    if conn:
        return conn

# Función para crear una tabla en la base de datos SQLite
def create_table(conn):
    try:
        sql = '''CREATE TABLE creditcard(id integer PRIMARY KEY, cc_num VARCHAR(255) NOT NULL, 
        merchant VARCHAR(255) NOT NULL, category VARCHAR(255) NOT NULL, amt FLOAT NOT NULL,
        city VARCHAR(255) NOT NULL, state VARCHAR(255) NOT NULL, job VARCHAR(255) NOT NULL, 
        trans_date_trans_time DATETIME NOT NULL'''
        conn.execute(sql)
    except Error as e:
        print(e)

# Función para insertar datos en la base de datos SQLite
def insert_datos(conn, info):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO creditcard(cc_num, merchant, category, amt, city, state, job, trans_date_trans_time) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (info['cc_num'], info['merchant'], info['category'], info['amt'], info['city'], info['state'], info['job'], info['trans_date_trans_time']))
        conn.commit()
    except Error as e:
        print(e)

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
    conn = create_connection("bank.db")
    create_table(conn)
    insert_datos(conn, info)
    check_database(conn)
    return jsonify({'message': '¡Información guardada con éxito!'}), 201

if __name__ == '__main__':
    app.run(debug=True)