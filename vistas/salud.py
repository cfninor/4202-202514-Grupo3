from flask_restful import Resource
from .estado import CAIDA, INSTANCIA

class VistaSalud(Resource):
    def get(self):
        if CAIDA["value"]:
            return {"instancia": INSTANCIA, "estado": "CAIDO"}, 500
        return {"instancia": INSTANCIA, "estado": "FUNCIONANDO"}, 200
