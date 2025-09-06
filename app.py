from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from vistas import \
    VistaEstado, VistaPedido

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaEstado, '/estado')
api.add_resource(VistaPedido, '/pedido/<int:id_pedido>')