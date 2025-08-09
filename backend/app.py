"""
Backend Flask API para gestión de alumnos
"""
import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM alumnos ORDER BY id;')
    alumnos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(alumnos)

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM alumnos WHERE id = %s;', (id,))
    alumno = cur.fetchone()
    cur.close()
    conn.close()
    if alumno:
        return jsonify(alumno)
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

@app.route('/alumnos', methods=['POST'])
def add_alumno():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    edad = data.get('edad')
    if not nombre or not apellido or edad is None:
        return jsonify({'error': 'Datos incompletos'}), 400
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'INSERT INTO alumnos (nombre, apellido, edad) VALUES (%s, %s, %s) RETURNING *;',
        (nombre, apellido, edad)
    )
    nuevo_alumno = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(nuevo_alumno), 201

@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    edad = data.get('edad')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM alumnos WHERE id = %s;', (id,))
    alumno = cur.fetchone()
    if not alumno:
        cur.close()
        conn.close()
        return jsonify({'error': 'Alumno no encontrado'}), 404
    cur.execute(
        'UPDATE alumnos SET nombre = %s, apellido = %s, edad = %s WHERE id = %s RETURNING *;',
        (nombre, apellido, edad, id)
    )
    alumno_actualizado = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(alumno_actualizado)

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM alumnos WHERE id = %s;', (id,))
    alumno = cur.fetchone()
    if not alumno:
        cur.close()
        conn.close()
        return jsonify({'error': 'Alumno no encontrado'}), 404
    cur.execute('DELETE FROM alumnos WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Alumno eliminado'})

if __name__ == '__main__':
    app.run(debug=True)
