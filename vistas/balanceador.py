import os, itertools, time, requests
from flask import Response
from flask_restful import Resource

HEARTBEAT = os.getenv("HEARTBEAT_URL")
TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "1.2"))

rr = itertools.cycle([0,1,2,3,4,5,6,7,8,9])
last_decisions = []

def get_healthy():
    r = requests.get(HEARTBEAT)
    data = r.json()["Servicios"]
    healthy = [b for b, st in data.items() if st["healthy"]]
    return healthy, data

def choose_backend(healthy):
    idx = next(rr) % max(1, len(healthy))
    return healthy[idx] if healthy else None

class VistaPedido(Resource):
    def get(self, id_pedido):
        t0 = time.time()
        healthy = get_healthy()
        be = choose_backend(healthy)
        if not be:
            last_decisions.append({"t": t0, "target": None, "result": "no_healthy"})
            return {"error": "no healthy backends"}, 503
        try:
            r = requests.get(f"{be}/pedido/{id_pedido}", timeout=TIMEOUT)
            last_decisions.append({"t": t0, "target": be, "result": r.status_code})
            # Propagamos payload y código tal cual
            return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type","application/json"))
        except Exception:
            last_decisions.append({"t": t0, "target": be, "result": "timeout"})
            return {"error": "backend timeout", "target": be}, 504

class VistaEstado(Resource):
    def get(self):
        try:
            healthy, snapshot = get_healthy()
        except Exception:
            healthy, snapshot = [], {}
        return {
            "healthy_backends": healthy,
            "snapshot": snapshot,
            "recent": last_decisions[-20:],
        }
