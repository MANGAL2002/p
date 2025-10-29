from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "subjects")

import os
import pymysql

def get_database_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def get_all_scp():
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM scp_subjects")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"scp data": data})

@app.route('/scp', methods=['POST'])
def add_scp():
    new_data = request.get_json()
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scp_subjects (item, class, description, containment) VALUES (%s, %s, %s, %s)",
        (new_data['item'], new_data['class'], new_data['description'], new_data['containment'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "SCP added successfully"})

@app.route('/scp/<int:id>', methods=['PUT'])
def update_scp(id):
    update_data = request.get_json()
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE scp_subjects SET item=%s, class=%s, description=%s, containment=%s WHERE id=%s",
        (update_data['item'], update_data['class'], update_data['description'], update_data['containment'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "SCP updated successfully"})

@app.route('/scp/<int:id>', methods=['DELETE'])
def delete_scp(id):
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM scp_subjects WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "SCP deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
