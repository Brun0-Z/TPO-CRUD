'''
Este código importa diferentes módulos y clases necesarios para el desarrollo de una aplicación Flask.

Flask: Es la clase principal de Flask, que se utiliza para crear instancias de la aplicación Flask.
jsonify: Es una función que convierte los datos en formato JSON para ser enviados como respuesta desde la API.
request: Es un objeto que representa la solicitud HTTP realizada por el cliente.
CORS: Es una extensión de Flask que permite el acceso cruzado entre dominios (Cross-Origin Resource Sharing), lo cual es útil cuando se desarrollan aplicaciones web con frontend y backend separados.
SQLAlchemy: Es una biblioteca de Python que proporciona una abstracción de alto nivel para interactuar con bases de datos relacionales.
Marshmallow: Es una biblioteca de serialización/deserialización de objetos Python a/desde formatos como JSON.
Al importar estos módulos y clases, estamos preparando nuestro entorno de desarrollo para utilizar las funcionalidades que ofrecen.

'''
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow

'''
En este código, se está creando una instancia de la clase Flask y se está configurando para permitir el acceso cruzado entre dominios utilizando el módulo CORS.

app = Flask(__name__): Se crea una instancia de la clase Flask y se asigna a la variable app. El parámetro __name__ es una variable que representa el nombre del módulo o paquete en el que se encuentra este código. Flask utiliza este parámetro para determinar la ubicación de los recursos de la aplicación.

CORS(app): Se utiliza el módulo CORS para habilitar el acceso cruzado entre dominios en la aplicación Flask. Esto significa que el backend permitirá solicitudes provenientes de dominios diferentes al dominio en el que se encuentra alojado el backend. Esto es útil cuando se desarrollan aplicaciones web con frontend y backend separados, ya que permite que el frontend acceda a los recursos del backend sin restricciones de seguridad del navegador. Al pasar app como argumento a CORS(), se configura CORS para aplicar las políticas de acceso cruzado a la aplicación Flask representada por app.

'''
# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

'''
En este código, se están configurando la base de datos y se están creando objetos para interactuar con ella utilizando SQLAlchemy y Marshmallow.

app.config["SQLALCHEMY_DATABASE_URI"]: Se configura la URI (Uniform Resource Identifier) de la base de datos. En este caso, se está utilizando MySQL como el motor de base de datos, el usuario y la contraseña son "root", y la base de datos se llama "proyecto". Esta configuración permite establecer la conexión con la base de datos.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]: Se configura el seguimiento de modificaciones de SQLAlchemy. Al establecerlo en False, se desactiva el seguimiento automático de modificaciones en los objetos SQLAlchemy, lo cual mejora el rendimiento.

db = SQLAlchemy(app): Se crea un objeto db de la clase SQLAlchemy, que se utilizará para interactuar con la base de datos. Este objeto proporciona métodos y funcionalidades para realizar consultas y operaciones en la base de datos.

ma = Marshmallow(app): Se crea un objeto ma de la clase Marshmallow, que se utilizará para serializar y deserializar objetos Python a JSON y viceversa. Marshmallow proporciona una forma sencilla de definir esquemas de datos y validar la entrada y salida de datos en la aplicación. Este objeto se utilizará para definir los esquemas de los modelos de datos en la aplicación.

'''
# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://vrunn0:lacaca.22@vrunn0.mysql.pythonanywhere-services.com/vrunn0$proyecto"
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = SQLAlchemy(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)

class Cancha(db.Model):  # Cancha hereda de db.Model
    """
    Definición de la tabla Cancha en la base de datos.
    La clase Cancha hereda de db.Model.
    Esta clase representa la tabla "cancha" en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    tipo = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, nombre, precio, tipo, imagen):
        """
        Constructor de la clase Producto.

        Args:
            nombre (str): Nombre del producto.
            precio (int): Precio del producto.
            tipo (int): Indica si es de F5 o F7.
            imagen (str): URL o ruta de la imagen del producto.
        """
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.imagen = imagen

    # Se pueden agregar más clases para definir otras tablas en la base de datos

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Producto
class CanchaSchema(ma.Schema):
    """
    Esquema de la clase Cancha.

    Este esquema define los campos que serán serializados/deserializados
    para la clase Cancha.
    """
    class Meta:
        fields = ("id", "nombre", "precio", "tipo", "imagen")

cancha_schema = CanchaSchema()  # Objeto para serializar/deserializar un producto
canchas_schema = CanchaSchema(many=True)  # Objeto para serializar/deserializar múltiples productos

'''
Este código define un endpoint que permite obtener todos los productos de la base de datos y los devuelve como un JSON en respuesta a una solicitud GET a la ruta /productos.
@app.route("/productos", methods=["GET"]): Este decorador establece la ruta /productos para este endpoint y especifica que solo acepta solicitudes GET.
def get_Productos(): Esta es la función asociada al endpoint. Se ejecuta cuando se realiza una solicitud GET a la ruta /productos.
all_productos = Producto.query.all(): Se obtienen todos los registros de la tabla de productos mediante la consulta Producto.query.all(). Esto se realiza utilizando el modelo Producto que representa la tabla en la base de datos. El método query.all() heredado de db.Model se utiliza para obtener todos los registros de la tabla.
result = productos_schema.dump(all_productos): Los registros obtenidos se serializan en formato JSON utilizando el método dump() del objeto productos_schema. El método dump() heredado de ma.Schema se utiliza para convertir los objetos Python en representaciones JSON.
return jsonify(result): El resultado serializado en formato JSON se devuelve como respuesta al cliente utilizando la función jsonify() de Flask. Esta función envuelve el resultado en una respuesta HTTP con el encabezado Content-Type establecido como application/json.

'''
@app.route("/cancha", methods=["GET"])
def get_Canchas():
    """
    Endpoint para obtener todos los productos de la base de datos.

    Retorna un JSON con todos los registros de la tabla de productos.
    """
    all_canchas = Cancha.query.all()  # Obtiene todos los registros de la tabla de productos
    result = canchas_schema.dump(all_canchas)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

'''
El código que sigue a continuación termina de resolver la API de gestión de productos, a continuación se destaca los principales detalles de cada endpoint, incluyendo su funcionalidad y el tipo de respuesta que se espera.
Endpoints de la API de gestión de productos:
get_producto(id):
    # Obtiene un producto específico de la base de datos
    # Retorna un JSON con la información del producto correspondiente al ID proporcionado
delete_producto(id):
    # Elimina un producto de la base de datos
    # Retorna un JSON con el registro eliminado del producto correspondiente al ID proporcionado
create_producto():
    # Crea un nuevo producto en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto
    # Retorna un JSON con el nuevo producto creado
update_producto(id):
    # Actualiza un producto existente en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado
    # Retorna un JSON con el producto actualizado

'''
@app.route("/cancha/<id>", methods=["GET"])
def get_cancha(id):
    """
    Endpoint para obtener un producto específico de la base de datos.

    Retorna un JSON con la información del producto correspondiente al ID proporcionado.
    """
    cancha = Cancha.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    return cancha_schema.jsonify(cancha)  # Retorna el JSON del producto

@app.route("/cancha/<id>", methods=["DELETE"])
def delete_cancha(id):
    """
    Endpoint para eliminar un producto de la base de datos.

    Elimina el producto correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    cancha = Cancha.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    db.session.delete(cancha)  # Elimina el producto de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return cancha_schema.jsonify(cancha)  # Retorna el JSON del producto eliminado

@app.route("/cancha", methods=["POST"])  # Endpoint para crear un producto
def create_cancha():
    """
    Endpoint para crear un nuevo producto en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto en la base de datos.
    Retorna un JSON con el nuevo producto creado.
    """
    nombre = request.json["nombre"]  # Obtiene el nombre del producto del JSON proporcionado
    precio = request.json["precio"]  # Obtiene el precio del producto del JSON proporcionado
    tipo = request.json["tipo"]  # Obtiene el stock del producto del JSON proporcionado
    imagen = request.json["imagen"]  # Obtiene la imagen del producto del JSON proporcionado
    new_cancha = Cancha(nombre, precio, tipo, imagen)  # Crea un nuevo objeto Producto con los datos proporcionados
    db.session.add(new_cancha)  # Agrega el nuevo producto a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return cancha_schema.jsonify(new_cancha)  # Retorna el JSON del nuevo producto creado

@app.route("/cancha/<id>", methods=["PUT"])  # Endpoint para actualizar un producto
def update_cancha(id):
    """
    Endpoint para actualizar un producto existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado.
    Retorna un JSON con el producto actualizado.
    """
    cancha = Cancha.query.get(id)  # Obtiene el producto existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    cancha.nombre = request.json["nombre"]
    cancha.precio = request.json["precio"]
    cancha.tipo = request.json["tipo"]
    cancha.imagen = request.json["imagen"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return cancha_schema.jsonify(cancha)  # Retorna el JSON del producto actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)