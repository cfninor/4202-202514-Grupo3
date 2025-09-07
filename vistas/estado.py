import os, time, requests, threading
from flask_restful import Resource

SERVICIOS = [b.strip() for b in os.getenv("SERVICIOS","").split(",") if b.strip()]
INTERVALOS = float(os.getenv("CHECK_INTERVAL_SEC", "1.0"))
ESTADO = {b: {"healthy": False} for b in SERVICIOS}
RUNNING = {"activo": False}

def verificar():
    while True:
        if not RUNNING["activo"]:
            time.sleep(INTERVALOS)
            continue
        for b in SERVICIOS:
            ok = False
            try:
                r = requests.get(f"{b}/salud")
                ok = r.status_code == 200
            except Exception:
                ok = False
            ESTADO[b] = {"healthy": ok}
        time.sleep(INTERVALOS)

threading.Thread(target=verificar, daemon=True).start()

class VistaEstado(Resource):
    def get(self):
        return {"Servicios": ESTADO}
    
class VistaControl(Resource):
    def post(self, estado):
        if estado == "arrancar":
            RUNNING["activo"] = True
            return {"estado": "experimento activado"}
        elif estado == "parar":
            RUNNING["activo"] = False
            return {"estado": "experimento detenido"}
        else:
            return {"error": "estado inválido"}, 400
