import os, json, time, threading
from io import BytesIO
from flask import Blueprint, request, jsonify, abort, send_file
from extensions import db
import pandas as pd, requests
from dateutil import tz
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from modelos import Usuario, Hallazgo

bp = Blueprint("detector", __name__)
ADMIN_SECRET = os.getenv("ADMIN_SECRET","detector-admin-secret")
AUDITOR_URL  = os.environ["AUDITOR_URL"]
EVENTOS_URL = f"{AUDITOR_URL}/eventos"
HUELLAS_URL = f"{AUDITOR_URL}/huellas"
ALERTAS_URL = os.environ["ALERTAS_URL"]
IP_DIAS_VIGENTES = int(os.getenv("IP_DIAS_VIGENTES","30"))
IP_DIVERSIDAD_UMBRAL = int(os.getenv("IP_DIVERSIDAD_UMBRAL","5"))
RUN = {"on": False}

REGLAS = {
  "fuera_horario": {"inicio": 6, "fin": 22},
  "rate_por_min": {"usuario": 30, "ip": 60},
  "corroboracion_minima": 1
}

def _tiempo_local(ts, tzname):
    z = tz.gettz(tzname or "UTC")
    return pd.Timestamp(ts).tz_localize("UTC").tz_convert(z).hour

def _validar_rol(df, anomalia, intentos):
    a_rol = df[(df.token_valido == True) & (df.autorizado == False)]
    if not a_rol.empty:
        a_rol = a_rol.copy();
        a_rol["regla"] = "rol_no_pertenece";
        anomalia = pd.concat([anomalia, a_rol])
        intentos.add("rol_no_pertenece")
        
def _validar_horario(df, anomalia, intentos):
    regla_horario = REGLAS["fuera_horario"]
    a_horario = df[(df.hora_local < regla_horario["inicio"]) | (df.hora_local > regla_horario["fin"])]
    if not a_horario.empty:
        a_horario = a_horario.copy();
        a_horario["regla"] = "usuario_fuera_horario";
        anomalia = pd.concat([anomalia, a_horario])
        intentos.add("usuario_fuera_horario")
        
def _validar_intentos_min(df, anomalia, intentos):
    ## PENDIENTE
    pass

def _detectar_anomalias():
    try:
        eventos = requests.get(EVENTOS_URL, timeout=5).json()
    except Exception:
        return 0
    if not eventos:
        return 0
    df = pd.DataFrame(eventos)
    try:
        usuario = pd.read_sql(Usuario.query.statement, db.session.bind)[["usuario","zona_horaria"]]
        df = df.merge(usuario, how="left", on="usuario")
    except Exception: 
        df["zona_horaria"] = "UTC"
    
    df["hora_local"] = [_tiempo_local(ts, tz) for ts, tz in zip(df["ts_utc"], df["zona_horaria"])]
    anomalia = pd.DataFrame();
    intentos = set()
    _validar_rol(df, anomalia, intentos)
    _validar_horario(df, anomalia, intentos)
    _validar_intentos_min(df, anomalia, intentos)
    

@bp.route("/admin/init", methods=["POST"])
def admin_init():
    if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
    db.create_all(); return {"ok": True}

@bp.route("/reglas", methods=["GET","POST"])
def reglas():
    if request.method=="POST":
        if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
        REGLAS.update(request.get_json(force=True))
    return jsonify({**REGLAS, "IP_DIAS_VIGENTES": IP_DIAS_VIGENTES,
                    "IP_DIVERSIDAD_UMBRAL": IP_DIVERSIDAD_UMBRAL})
    
@bp.route("/")
def health(): return {"ok": True}