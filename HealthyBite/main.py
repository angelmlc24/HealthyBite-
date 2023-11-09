from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


DB_PATH = 'base_de_datos/HealthyBite.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear tabla Cliente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente(
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            contraseña TEXT,
            email TEXT,
            telefono TEXT
        )
    ''')

    # Crear tabla Plato_Favorito
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Plato_Favorito(
            id_favorito INTEGER PRIMARY KEY,
            id_cliente INTEGER,
            id_plato INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
            FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
        )
    ''')

    # Crear tabla Pedido
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedido(
            id_pedido INTEGER PRIMARY KEY,
            fecha_pedido TEXT,
            estado_del_pedido TEXT,
            precio_total REAL,
            id_cliente INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        )
    ''')

    # Crear tabla Plato
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Plato(
            id_plato INTEGER PRIMARY KEY,
            nombre_plato TEXT,
            descripcion TEXT,
            categoria TEXT,
            id_pedido INTEGER,
            FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido)
        )
    ''')

    # Crear tabla Comentario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Comentario(
            id_comentario INTEGER PRIMARY KEY,
            id_cliente INTEGER,
            id_plato INTEGER,
            comentario_de_cliente TEXT,
            puntuacion INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
            FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
        )
    ''')

    # Crear tabla Notificacion
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notificacion(
            id_notificacion INTEGER PRIMARY KEY,
            id_cliente INTEGER,
            contenido_de_notif TEXT,
            tipo TEXT,
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        )
    ''')

    # Crear tabla FAQ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FAQ(
            id_faq INTEGER PRIMARY KEY,
            pregunta TEXT,
            respuesta TEXT
        )
    ''')

    # Crear tabla Restriccion_dietetica
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restriccion_dietetica(
            id_restriccion INTEGER PRIMARY KEY,
            nombre_restriccion TEXT,
            descripcion TEXT,
            informacion_nutricional TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Funciones para verificar y registrar usuarios
def verificar_existencia_usuario(nombre, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Cliente WHERE nombre = ?", (nombre,))
    count = cursor.fetchone()[0]
    return count > 0

def verificar_credenciales(nombre, contraseña, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Cliente WHERE nombre = ? AND contraseña = ?", (nombre, contraseña))
    count = cursor.fetchone()[0]
    return count > 0

def registrar_cliente(nombre, contraseña, email, telefono, conn):
    if verificar_existencia_usuario(nombre, conn):
        return "El nombre de usuario ya está en uso. Por favor, elige otro nombre de usuario."
    else:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Cliente (nombre, contraseña, email, telefono) VALUES (?, ?, ?, ?)", (nombre, contraseña, email, telefono))
        conn.commit()
        return "Registro exitoso. ¡Gracias por registrarte!"

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Rutas de registro y login
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        conn = get_db_connection()
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        email = request.form['email']
        telefono = request.form['telefono']
        mensaje = registrar_cliente(nombre, contraseña, email, telefono, conn)
        conn.close()
        if mensaje.startswith("El nombre de usuario ya está en uso."):
            return mensaje
        else:
            return redirect(url_for('registro_exitoso'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        nombre = request.form['nombre']
        contraseña = request.form['contraseña']
        if verificar_credenciales(nombre, contraseña, conn):
            conn.close()
            return redirect(url_for('inicio'))
        else:
            conn.close()
            return redirect(url_for('login_incorrecto'))
    return render_template('login.html')


@app.route('/registro_exitoso')
def registro_exitoso():
    return render_template('registro_exitoso.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/login_incorrecto')
def login_incorrecto():
    return render_template('login_incorrecto.html')


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=81)
  