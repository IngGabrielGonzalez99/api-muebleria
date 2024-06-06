from bson import ObjectId
from app import create_app
from mongo import mongo
#from flask import Blueprint, jsonify, request
from flask import Blueprint, jsonify, request
from  bson.json_util import dumps

prod = Blueprint ("productos", __name__)
app = create_app()

@prod.route('/productos/get_all', methods=['GET'])
def listar_prod():
    data=mongo.db.productos.find({})
    r=dumps(data)
    return  r

@prod.route('/productos/porNombre/<string:nombre>', methods=['GET'])
def Obtener_PorNombre(nombre):
    query={'nombre': {'$eq':nombre}}
    sort = [('nombre', 1)]
    project= { "_id": 0,"nombre":1, "precio":1, "descripcion":1}
    try:
        resultado = mongo.db.productos.find(query,project).sort(sort)
        if resultado:
            #
            return jsonify(list(resultado))
        else:
            #
            return jsonify({"mensaje": "Documento no encontrado"}), 404
        
    except Exception as e:
        #Manejo de la expresion, puedes personalzar el mensaje de error segun tus 
        return jsonify({"error": str(e)}), 500
    
@prod.route('/productos/eliminar/<string:id>', methods=['DELETE'])
def eliminar_PorID(id):
  try:
    resultado = mongo.db.productos.delete_one({'_id': id})
    return jsonify({"Mensaje:": "Objeto eliminado"})
  except Exception as e:
    return jsonify({"Mensaje": "Objeto eliminado"})

@prod.route('/productos/porID/<string:_id>', methods=['GET'])
def Obtener_PorID(_id):
    query={'_id': _id}
    project= {"_id":0, "nombre":1, "costo ": 1, "precio:": 1, "descripcion":1}
    try:
        resultado = mongo.db.productos.find(query,project)
        if resultado:
            #Si la consulta es exitosa , devuelve los datos en fromato Json 
            return jsonify(dumps(resultado))
        else:
            #Si no se encuentra el documento, devuelve un mensaje adecuado 
            return jsonify({"mensaje": "Documento no encontrado"}), 404
        
    except Exception as e:
        #Manejo de la expresion, puedes personalzar el mensaje de error segun tus 
        return jsonify({"error": str(e)}), 500
    
@prod.route('/productos/prod_prov', methods=['GET'])
def Obtener_Prod_prov():
    query=[
  {
    '$lookup': {
      'from': "proveedor",
      'localField': "provId",
      'foreignField': "_id",
      'as': "proveedor"
    }
  },
  {
    '$unwind': "$proveedor"
  },
  {
    '$project': {
      "_id": 1,
      "nombProd": 1,
      "precio": 1,
      "caracteristicas": 1,
      "proveedor.RFC": 1,
      "proveedor.nombreProveedor": 1
    }
  }
]
    try:
        resultado = mongo.db.productos.aggregate(query)
        if resultado:
            #
            return dumps(list(resultado))
        else:
            #
            return jsonify({"mensaje": "Documento no encontrado"}), 404
        
    except Exception as e:
        #Manejo de la expresion, puedes personalzar el mensaje de error segun tus 
        return jsonify({"error": str(e)}), 500
      
      
#Nueva ruta:
@prod.route('/productos/nuevoProd', methods=['POST'])
def add_producto():
  #from flask import request
  n=request.json["nombre"]
  
  #Objeto categoría
  cat=request.json["categoria"]["nombreCat"]
  catDos=request.json["categoria"]["zona"]
  catTres=request.json["categoria"]["descripcionCat"]
  
  #Objeto marca
  mc=request.json["marca"]["nombremarca"]
  mcDos=request.json["marca"]["modelo"]
  
  costo=request.json["costo"]
  
  precio = request.json["precio"]
  
  #Objeto dimensiones
  dimensionesLargo = request.json["dimensiones"]["largo"]
  dimensionesAlto = request.json["dimensiones"]["alto"]
  dimensionesAncho = request.json["dimensiones"]["ancho"]
  
  color = request.json["color"]
  
  foto = request.json["foto"]
  fecha_adquisicion = request.json["fecha_adquisicion"]
  
  cantidad_existente = request.json["cantidad_existente"]
  
  status = request.json["status"]
  
  material_fabricacion = request.json["material_de_fabricacion"]
  
  #Objeto origen
  origenPais = request.json["origen"]["pais"]
  origenIdioma = request.json["origen"]["idioma"]
  
  marca_id = request.json["marca_id"]
  
  prov_id = request.json["prov_id"]
  


  if request.method=='POST':
    product={"nombre": n,
    "categoria":{"nombreCat":cat,"zona":catDos, "descripcionCat": catTres},
    "marca":{"nombremarca": mc, "modelo": mcDos},
    "costo":costo,
    "precio":costo + costo * 20/100,
    "dimensiones": {"largo": dimensionesLargo, "alto": dimensionesAlto, "ancho": dimensionesAncho},
    "color":color,
    "foto":foto,
    'fechaAdquisicion':fecha_adquisicion,
    "cantidad_existente": cantidad_existente,
    "status": status,
    "material_de_fabricacion": material_fabricacion,
    "origen": {"pais": origenPais, "idioma": origenIdioma},
    "marca_id": marca_id,
    "prov_id": prov_id}

  product1={"nombre":"Silla desde postman",
  "categoria":{"nombreCat":"consumibles","zona":"zona nueva", "descripcionCat": "descripcion desde postman"},
  "marca":{"nombremarca":"Marca Postman","modelo":"Modelo postman"},
  "costo": 150,
  "precio":"123",
  "estatus":"activo",
  "paisOrigen":"Alemania",
  "cantidadExistente":123,
  "dimensiones":{"largo":"1.80","alto":"1.20", "ancho": "1.57"},
  "color": "verde",
  "foto": "imagen.jpg",
  "fecha_adquisicion": "2023-12-24",
  "cantidad_existente": 45,
  "status": "vigente",
  "material_de_fabricacion": "cemento",
  "origen":{"pais":"Mexico","idioma":"Español"},
  "marca_id": 2,
  "prov_id": 2}

  try:
    resultado = mongo.db.productos.insert_one(product)
    if resultado:
      return jsonify({"mensaje": "Documento insertado"})
    else:
      return jsonify({"mensaje": "Documento no insertado"}), 404
  except Exception as e:
    return jsonify({"error": str(e)}), 500
  
  
  #NUEVA
@prod.route('/productos/actualizar/<string:id>', methods=["put"])
def actualizar_costo(id):
  nuevo_costo=request.json["costo"]

  try:
      resultado = mongo.db.productos.update_one({'_id':(id)}, {"$set": {"costo": nuevo_costo}})
      if resultado:
        #Si la consulta es exisota, devuelve los datos en formato JSON
        actualizar_precio(id, nuevo_costo)
        return jsonify({"mensaje:": "Documento actualizado"})
      else:
        #Si no se encuentra el documento, devuelve un mensaje adecuado
        return jsonify({"mensaje": "Documento no encontrado"}), 404
  except Exception as e:
    #Manejo de excepción, puedes personalizar el mensaje de error según
    #tus necesidades
    return jsonify({"Error:": str(e)}), 500

def actualizar_precio (id, nuevo_costo):
  try:
    resultado = mongo.db.productos.update_one({'_id': (id)}, {"$set": {"precio": nuevo_costo + (nuevo_costo * 20/100)}})
    if resultado:
      #Si la consulta es exitosa, devuelve los datos en formato json
      return jsonify({"Mensaje:": "Precio actualizado"})
    else:
      #Si la consulta no es exisota
      return jsonify({"Mensaje": "El precio no fue actualizado"})
  except Exception as e:
    #Manejar las excepciones según las necesidades
    return jsonify({"Error:": str(e)}), 500

