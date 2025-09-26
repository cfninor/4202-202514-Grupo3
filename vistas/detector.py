import os, json, time, threading
from io import BytesIO
from flask import Blueprint, request, jsonify, abort, send_file, current_app
from extensions import db
import pandas as pd, requests
from dateutil import tz
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from modelos import Usuario, Hallazgo
import logging

bp = Blueprint("detector", __name__)
ADMIN_SECRET = os.getenv("ADMIN_SECRET","detector-admin-secret")
AUDITOR_URL  = os.environ["AUDITOR_URL"]
EVENTOS_URL = f"{AUDITOR_URL}/eventos"
HUELLAS_URL = f"{AUDITOR_URL}/huellas"
ALERTAS_URL = os.environ["ALERTAS_URL"]
IP_DIAS_VIGENTES = int(os.getenv("IP_DIAS_VIGENTES","30"))
IP_DIVERSIDAD_UMBRAL = int(os.getenv("IP_DIVERSIDAD_UMBRAL","1"))
RUN = {"on": False, "wm_ts": None}
log = logging.getLogger(__name__)

REGLAS = {
  "fuera_horario": {"inicio": 6, "fin": 22},
  "rate_por_min": {"usuario": 30, "ip": 60},
  "corroboracion_minima": 1
}

def _tiempo_local(ts, tzname):
    z = tz.gettz(tzname or "UTC") or tz.gettz("UTC")
    t = pd.Timestamp(ts)
    if t.tzinfo is None:
        t = t.tz_localize("UTC")
    else:
        pass
    return t.tz_convert(z).hour

def _validar_rol(df, anomalia, intentos):
    a_rol = df[(df.token_valido == True) & (df.autorizado == False)]
    if not a_rol.empty:
        a_rol = a_rol.copy();
        a_rol["regla"] = "rol_no_pertenece";
        anomalia = pd.concat([anomalia, a_rol])
        intentos.add("rol_no_pertenece")
    return anomalia
        
def _validar_horario(df, anomalia, intentos):
    regla_horario = REGLAS["fuera_horario"]
    a_horario = df[(df.hora_local < regla_horario["inicio"]) | (df.hora_local > regla_horario["fin"])]
    if not a_horario.empty:
        a_horario = a_horario.copy();
        a_horario["regla"] = "usuario_fuera_horario";
        anomalia = pd.concat([anomalia, a_horario])
        intentos.add("usuario_fuera_horario")
    return anomalia
        
def _validar_intentos_min(df, anomalia, intentos):
    df["min"] = pd.to_datetime(df["ts_utc"]).dt.floor("min")
    gu = df.groupby(["usuario","min"]).size().reset_index(name="c")
    ku = gu[gu.c > REGLAS["rate_por_min"]["usuario"]][["usuario","min"]]
    if not ku.empty:
        a_intentos_usuario = df.merge(ku,on=["usuario","min"]); a_intentos_usuario["regla"]="rate_usuario_alto"; anomalia=pd.concat([anomalia,a_intentos_usuario]); intentos.add("rate_usuario_alto")
    gi = df.groupby(["ip","min"]).size().reset_index(name="c")
    ki = gi[gi.c > REGLAS["rate_por_min"]["ip"]][["ip","min"]]
    if not ki.empty:
        a_intentos_ip = df.merge(ki,on=["ip","min"]); a_intentos_ip["regla"]="rate_ip_alto"; anomalia=pd.concat([anomalia,a_intentos_ip]); intentos.add("rate_ip_alto")
    return anomalia
    
def _validar_ip_dias(df, anomalia, intentos):
    hu = requests.get(HUELLAS_URL+"?limit=50000", timeout=5).json()
    hu = pd.DataFrame(hu)
    if not hu.empty:
        hu["ultima_vez"] = pd.to_datetime(hu["ultima_vez"], utc=True, errors="coerce")
        cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=IP_DIAS_VIGENTES)
        recientes = (
            hu.loc[hu["ultima_vez"].notna() & (hu["ultima_vez"] >= cutoff), ["usuario", "ip"]]
              .drop_duplicates()
        )
        k = df[["usuario","ip"]].drop_duplicates()
        m = k.merge(recientes, on=["usuario","ip"], how="left", indicator=True)
        nuevas = m[m["_merge"]=="left_only"][["usuario","ip"]]
        if not nuevas.empty:
            a_ip = df.merge(nuevas,on=["usuario","ip"]); 
            a_ip["regla"]="ip_nueva_usuario";
            anomalia=pd.concat([anomalia,a_ip]);
            intentos.add("ip_nueva_usuario");
    return anomalia
            
def _validar_ip_min(df, anomalia, intentos):
    win = pd.to_datetime(df["ts_utc"]).max() - pd.Timedelta(minutes=10)
    d10 = df[pd.to_datetime(df["ts_utc"])>=win]
    div = d10.groupby("usuario")["ip"].nunique().reset_index(name="n")
    sosp = div[div.n>IP_DIVERSIDAD_UMBRAL]["usuario"]
    if not sosp.empty:
        a_ip_min = d10[d10["usuario"].isin(sosp)].copy(); a_ip_min["regla"]="ip_diversa_usuario"
        anomalia=pd.concat([anomalia,a_ip_min]); intentos.add("ip_diversa_usuario")
    return anomalia
    
def _validar_concurrencia(df, anomalia, intentos, ventana="10s"):
    if df.empty:
        return anomalia
    df_con = df.copy()
    df_con["ts_utc"] = pd.to_datetime(df_con["ts_utc"], utc=True, errors="coerce")
    df_con = df_con[df_con["ts_utc"].notna()]
    df_con["ts_bucket"] = df_con["ts_utc"].dt.round(ventana)
    conc = (df_con.groupby(["usuario", "ts_bucket"])["ip"]
              .nunique()
              .reset_index(name="n"))
    conc = conc[conc["n"] >= 2][["usuario", "ts_bucket"]]
    if not conc.empty:
        a_concurrencia = df_con.merge(conc, on=["usuario", "ts_bucket"], how="inner")
        a_concurrencia = a_concurrencia.copy();
        a_concurrencia["regla"] = "concurrent_ips_usuario";
        anomalia = pd.concat([anomalia, a_concurrencia], ignore_index=True, sort=False) 
        intentos.add("concurrent_ips_usuario")
    return anomalia
    
def _detectar_anomalias():
    try:
        eventos = requests.get(EVENTOS_URL, timeout=5).json()
    except Exception:
        return 0
    if not eventos:
        return 0
    df = pd.DataFrame(eventos)
    df["ts_utc"] = pd.to_datetime(df["ts_utc"], utc=True, errors="coerce")
    df = df[df["ts_utc"].notna()]
    wm = RUN.get("wm_ts")
    if wm is not None:
        df = df[df["ts_utc"] > wm]
    if df.empty:
        return 0
    
    try:
        usuario = pd.read_sql(Usuario.query.statement, db.session.bind)[["usuario","zona_horaria"]]
        df = df.merge(usuario, how="left", on="usuario")
    except Exception: 
        df["zona_horaria"] = "UTC"
    
    df["hora_local"] = [_tiempo_local(ts, tz) for ts, tz in zip(df["ts_utc"], df["zona_horaria"])]
    anomalia = pd.DataFrame();
    intentos = set()
    anomalia =_validar_rol(df, anomalia, intentos)
    anomalia = _validar_horario(df, anomalia, intentos)
    anomalia = _validar_intentos_min(df, anomalia, intentos)
    anomalia = _validar_ip_dias(df, anomalia, intentos)
    anomalia = _validar_ip_min(df, anomalia, intentos)
    anomalia = _validar_concurrencia(df, anomalia, intentos)
    
    if not anomalia.empty:
        cols_dedupe = [c for c in ["usuario","ip","ts_utc","recurso","metodo","regla"] if c in anomalia.columns]
        anomalia = anomalia.drop_duplicates(subset=cols_dedupe, keep="first", ignore_index=True)
    total = len(anomalia)
    if total and len(intentos) >= REGLAS["corroboracion_minima"]:
        muestra = json.loads(
            anomalia.head(30).to_json(orient="records", date_format="iso")
        )
        db.session.add(Hallazgo(
            regla="detector", severidad="medio",
            total_eventos=int(total),
            muestra_json=json.dumps(muestra, ensure_ascii=False)
        ));
        db.session.commit()
        try:
            requests.post(ALERTAS_URL, json={"titulo":"Anomalías detectadas",
                "detalle":{"total":int(total), "reglas":list(intentos), "muestra":muestra}}, timeout=3)
        except Exception as e:
            log.warning(f"No se pudo enviar alerta: {e}")
    RUN["wm_ts"] = max(RUN["wm_ts"], df["ts_utc"].max()) if RUN.get("wm_ts") is not None else df["ts_utc"].max()
    return total

def _loop():
    while RUN["on"]:
        try:
            _detectar_anomalias()
            db.session.remove()
        except Exception as e:
            log.exception(f"Fallo en loop de detección: {e}")
        time.sleep(5)
        
def _loop_with_app(app):
    with app.app_context():
        _loop()
        
@bp.route("/admin/start", methods=["POST"])
def admin_start():
    if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
    if not RUN["on"]:
        app = current_app._get_current_object()
        RUN["on"]=True; threading.Thread(target=_loop_with_app, args=(app,), daemon=True).start()
    return {"running": RUN["on"]}

@bp.route("/admin/stop", methods=["POST"])
def admin_stop():
    if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
    RUN["on"]=False; return {"running": RUN["on"]}

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
    
@bp.route("/charts/eventos_por_min.png")
def chart_ev_min():
    try:
        evs = requests.get(EVENTOS_URL, timeout=5).json()
        if not evs: abort(404)
        df = pd.DataFrame(evs); df["t"]=pd.to_datetime(df["ts_utc"])
        s = df.set_index("t").resample("1min").size()
        plt.figure(figsize=(6,3)); s.plot(); plt.title("Eventos por minuto")
        plt.xlabel("Tiempo"); plt.ylabel("Eventos")
        buf = BytesIO(); plt.tight_layout(); plt.savefig(buf, format="png"); buf.seek(0)
        return send_file(buf, mimetype="image/png")
    except Exception: 
        abort(500)
    
@bp.route("/")
def health(): return {"ok": True}