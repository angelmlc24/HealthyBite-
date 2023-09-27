import datetime
import pytz  # para manejar la zona horaria

class Cliente:
    def __init__(self, id, nombre, correo_electronico):
        self.id = id
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.pedidos = []
        self.favoritos = []
        self.comentarios = []
        self.notificaciones = []
        self.preguntas_frecuentes = []

class Pedido:
    def __init__(self, id, fecha_hora, estado, total):
        self.id = id
        self.fecha_hora = fecha_hora
        self.estado = estado
        self.total = total
        self.cliente = None  # Referencia al cliente que realizó el pedido
        self.platos = []

class Plato:
    def __init__(self, id, nombre, descripcion, precio):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.restricciones_dieteticas = []

class RestriccionDietetica:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class Favorito:
    def __init__(self, cliente, plato):
        self.cliente = cliente
        self.plato = plato

class Comentario:
    def __init__(self, cliente, plato, texto, calificacion):
        self.cliente = cliente
        self.plato = plato
        self.texto = texto
        self.calificacion = calificacion

class Notificacion:
    def __init__(self, cliente, contenido, fecha_hora):
        self.cliente = cliente
        self.contenido = contenido
        self.fecha_hora = fecha_hora

class FAQ:
    def __init__(self, pregunta, respuesta, cliente):
        self.pregunta = pregunta
        self.respuesta = respuesta
        self.cliente = cliente

# Función para realizar un pedido
def realizar_pedido(cliente, plato):
    # Obtener la fecha y hora actual en la zona horaria de Buenos Aires
    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    fecha_hora_actual = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    # Crea un nuevo pedido con la fecha y hora actual
    pedido = Pedido(101, fecha_hora_actual, "En proceso", 0.0)
    pedido.cliente = cliente
    pedido.platos.append(plato)
    
    # Calcular el total del pedido (en este ejemplo, simplemente sumamos el precio del plato)
    for plato in pedido.platos:
        pedido.total += plato.precio
    
    cliente.pedidos.append(pedido)
    return pedido

# Ejemplo de uso:
cliente1 = Cliente(1, "Cliente 1", "cliente1@example.com")
plato1 = Plato(201, "Plato A", "Descripción del Plato A", 15.0)

# Realizar un pedido
pedido_realizado = realizar_pedido(cliente1, plato1)

# Mostrar el resumen del pedido en la consola
print("Resumen del Pedido:")
print(f"Cliente: {pedido_realizado.cliente.nombre}")
print(f"Fecha y Hora: {pedido_realizado.fecha_hora}")
print(f"Estado: {pedido_realizado.estado}")
print("Platos en el Pedido:")
for plato in pedido_realizado.platos:
    print(f"- {plato.nombre}: ${plato.precio}")
print(f"Total a pagar: ${pedido_realizado.total}")
