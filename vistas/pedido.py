import time
import random
from flask_restful import Resource
from .estado import CAIDA, INSTANCIA, LATENCIA

ESTADOS = ["PENDIENTE", "PROCESANDO", "ENVIADO", "ENTREGADO", "CANCELADO"]

class VistaPedido(Resource):
    def get(self, id_pedido):
        if CAIDA["value"]:
            time.sleep(3)
            return {"instancia": INSTANCIA, "error": "instancia caida"}, 503
        time.sleep(int(LATENCIA)/1000.0)
        return {
            "instancia": INSTANCIA,
            "pedidoId": id_pedido,
            "estado": random.choice(ESTADOS),
        }, 200