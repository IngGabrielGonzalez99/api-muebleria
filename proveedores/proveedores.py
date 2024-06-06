from mongo import mongo
from flask import Blueprint
from bson.json_util import dumps
#creación del módulo
prove=Blueprint("provee", __name__)

@prove.route('/proveedores/get_all', methods=['GET'])
def listar_prove():
    data=mongo.db.proveedores.find({})
    r=dumps(data)
    return r

@prove.route('/proveedores/porNombre/<string:nombre>', methods=['GET'])
def obtenerProve(nombre):
    data = mongo.db.proveedores.find({'nombreProveedor': nombre})
    r = dumps(data)
    return r