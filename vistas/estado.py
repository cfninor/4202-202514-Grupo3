import os
from flask import request
from flask_restful import Resource

INSTANCIA = os.getenv("INSTANCE_NAME", "pedido-desconocido")
CAIDA = {"value": False}
LATENCIA = os.getenv("LAT_MS", 20)

class VistaEstado(Resource):
    def get(self):
        bandera = request.args.get("on", "true").lower() == "true"
        CAIDA["value"] = bandera
        return {"instance": INSTANCIA, "caida": CAIDA["value"]}, 200
