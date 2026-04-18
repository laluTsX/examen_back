from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuración de Swagger visual
swagger = Swagger(app)

# Redirección automática: si entras a la raíz, te manda a la documentación
@app.route('/')
def index():
    return redirect('/apidocs/')

# --- CONEXIÓN A LA DB ---
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',           
        database='examen_back2' 
    )

# --- LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    """
    Login de usuario
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Éxito
    """
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == '1234':
        return jsonify({"message": "Login exitoso", "token": "jwt-py-123"}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401

# --- CRUD DE CURSOS Y FILTROS ---
@app.route('/courses', methods=['GET'])
def get_courses():
    """
    Listar cursos con filtros por categoría y fecha
    ---
    parameters:
      - name: categoria
        in: query
        type: integer
      - name: fecha_inicio
        in: query
        type: string
      - name: fecha_fin
        in: query
        type: string
    responses:
      200:
        description: Lista de cursos
    """
    categoria = request.args.get('categoria')
    f_inicio = request.args.get('fecha_inicio')
    f_fin = request.args.get('fecha_fin')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM cursos WHERE 1=1"
    params = []
    
    if categoria:
        sql += " AND categoria_id = %s"
        params.append(categoria)
    if f_inicio and f_fin:
        sql += " AND fecha_creacion BETWEEN %s AND %s"
        params.extend([f_inicio, f_fin])
        
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route('/courses', methods=['POST'])
def create_course():
    """
    Crear un nuevo curso
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
            descripcion:
              type: string
            categoria_id:
              type: integer
            precio:
              type: number
            fecha_creacion:
              type: string
    responses:
      201:
        description: Creado
    """
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO cursos (nombre, descripcion, categoria_id, precio, fecha_creacion) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (data['nombre'], data['descripcion'], data['categoria_id'], data['precio'], data['fecha_creacion']))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "message": "Curso creado"}), 201

# --- CATEGORÍAS ---
@app.route('/courses/categories', methods=['POST'])
def create_category():
    """
    Crear una categoría
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
    responses:
      201:
        description: Creada
    """
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Categoría creada"}), 201

if __name__ == '__main__':
    app.run(port=3000, debug=True)