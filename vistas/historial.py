import os, time, jwt, requests
import logging
from flask import Blueprint, request, jsonify

bp = Blueprint("autorizacion", __name__)
AUTH_URL = os.environ["AUTH_URL"]
AUDITOR_LOG_URL = os.environ["AUDITOR_LOG_URL"]
JWT_SECRET = os.getenv("JWT_SECRET","jwt-secret")
log = logging.getLogger(__name__)

def _client_ip(req):
    return req.headers.get("X-Forwarded-For", req.remote_addr) or "0.0.0.0"

def _audit(req, payload):
    try:
        requests.post(AUDITOR_LOG_URL, json=payload, headers={"X-Forwarded-For": _client_ip(req)}, timeout=2)
    except Exception as e:
        log.warning(f"No se pudo enviar el log al auditor: {e}")
    
@bp.route("/historial/<usuario>")
def historial(usuario):
    t0 = time.time()
    token = request.headers.get("Authorization","").replace("Bearer ","")
    token_valido, rol = False, None
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        token_valido, rol = True, data.get("rol")
    except Exception as e:
        log.warning(f"Token inválido: {e}")
    autorizado = False
    try:
        r = requests.post(AUTH_URL, json={"usuario":usuario,"rol":rol,"recurso":"historial"}, timeout=2)
        autorizado = (r.status_code == 200)
    except Exception as e:
        log.warning(f"Fallo al contactar a AUTH_URL: {e}")

    status = 200 if (token_valido and autorizado) else 403
    body = {"historial":["pedido-001","pedido-002"]} if status==200 else {"error":"No autorizado"}

    _audit(request, {
      "usuario": usuario, "rol": rol, "recurso":"historial", "metodo":"GET",
      "token_valido": token_valido, "autorizado": autorizado,
      "http_status": status, "lat_ms": int((time.time()-t0)*1000)
    })
    return jsonify(body), status

@bp.route("/")
def health(): return {"ok": True}