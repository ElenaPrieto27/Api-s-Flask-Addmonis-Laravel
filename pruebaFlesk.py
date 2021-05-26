from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/api_ele'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    Inf_Producto = db.Column(db.String(100))

    def __init__(self, nombre, Inf_Producto):
        self.nombre = nombre
        self.Inf_Producto = Inf_Producto

db.create_all()

class Taskchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'Inf_Producto')

product_schema = Taskchema()
products_schema = Taskchema(many=True)


#Ruta para insertar datos con post
@app.route('/task', methods=['POST'])
def create_product():

    nombre = request.json['nombre']
    Inf_Producto = request.json['Inf_Producto']

    new_product = producto(nombre, Inf_Producto)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


#Ruta para tener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():

    #Lista de las tareas y se guarda en la variable result
    all_tasks = producto.query.all()
    result = products_schema.dump(all_tasks)

    return jsonify(result)









if __name__ == "__main__":
    app.run(debug=True)