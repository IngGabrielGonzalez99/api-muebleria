from bson import ObjectId
from mongo import mongo
from flask import Blueprint, jsonify, request
from bson.json_util import dumps
#creación del módulo
marcas=Blueprint("marcas", __name__)

@marcas.route('/marcas/get_all', methods=['GET'])
def listar_prove():
    data=mongo.db.marca.find({})
    r=dumps(data)
    return r

@marcas.route('/marcas/porNombre/<string:nombre>', methods=['GET'])
def Obtener_PorNombre(nombre):
    query={'nombre': nombre}
    sort = [('nombre', 1)]
    project= { "_id": 0,"nombre":1}
    try:
        resultado = mongo.db.marcas.find(query,project).sort(sort)
        if resultado:
            #
            return jsonify(list(resultado))
        else:
            #
            return jsonify({"mensaje": "Documento no encontrado"}), 404
        
    except Exception as e:
        #Manejo de la expresion, puedes personalzar el mensaje de error segun tus 
        return jsonify({"error": str(e)}), 500

@marcas.route('/marcas/anadir')
def agregarMarca():
    nombre = request.json["nombre"]
    imagen = request.json["imagen"]
    rfc = request.json["RFC"]
    paginaWeb = request.json["paginaWeb"]
    
    if request.method=='POST':
        product = {
            "nombreMarca" : nombre,
            "logo": imagen,
            "RFC":  rfc,
            "paginaWeb": paginaWeb
        }
        
    try:
        resultado = mongo.db.marcas.insert_one(product)
        if resultado:
         return jsonify({"mensaje": "Documento insertado"})
        else:
            return jsonify({"mensaje": "Documento no insertado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@marcas.route('/marcas/eliminar/<string:id>', methods=['DELETE'])
def eliminar_PorID(id):
  try:
    resultado = mongo.db.marca.delete_one({'_id': ObjectId(id)})
    if resultado:
        return jsonify({"Mensaje": "Objeto eliminado"})
  except Exception as e:
    return jsonify({"Mensaje": "Error al eliminar el objeto: " + str(e)})

        