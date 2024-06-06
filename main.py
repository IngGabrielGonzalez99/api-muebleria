#main.py
from app import create_app
from productos import prod
from proveedores.proveedores import prove
from marcas.marcas import marcas
from flask_cors import CORS

app = create_app()
app.register_blueprint(prod)
app.register_blueprint(prove)
app.register_blueprint(marcas)
CORS(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)