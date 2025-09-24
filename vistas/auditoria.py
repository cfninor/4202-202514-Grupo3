import os, datetime
from flask import Blueprint, request, jsonify, abort
from extensions import db
from modelos import Evento, HuellaIP

bp = Blueprint("auditoria", __name__)
ADMIN_SECRET = os.getenv("ADMIN_SECRET","auditoria-admin-secret")
    
@bp.route("/admin/init", methods=["POST"])
def admin_init():
    if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
    db.create_all(); 
    return {"ok": True}

@bp.route("/log", methods=["POST"])
def log_evento():
    event = request.get_json(force=True)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "0.0.0.0"
    ev = Evento(
        ip=ip, user_agent=request.headers.get("User-Agent"),
        usuario=event.get("usuario"), rol_reportado=event.get("rol"),
        recurso=event.get("recurso","historial"), metodo=event.get("metodo","GET"),
        token_valido=bool(event.get("token_valido")),
        autorizado=bool(event.get("autorizado")),
        http_status=int(event.get("http_status",200)),
        lat_ms=int(event.get("lat_ms",0)),
        motivo=event.get("motivo")
    )
    db.session.add(ev)
    u = (event.get("usuario") or "").strip()
    if u:
        h = HuellaIP.query.filter_by(usuario=u, ip=ip).first()
        if h:
            h.ultima = datetime.datetime.now(datetime.timezone.utc); h.peticiones = (h.peticiones or 0)+1
        else:
            db.session.add(HuellaIP(usuario=u, ip=ip))
    db.session.commit()
    return {"ok": True}

@bp.route("/eventos")
def eventos():
    lim = int(request.args.get("limit","5000"))
    rows = Evento.query.order_by(Evento.ts_utc.desc()).limit(lim).all()
    return jsonify([{
        "ts_utc": r.ts_utc.isoformat(), "ip": r.ip, "usuario": r.usuario,
        "rol_reportado": r.rol_reportado, "recurso": r.recurso, "metodo": r.metodo,
        "token_valido": r.token_valido, "autorizado": r.autorizado,
        "http_status": r.http_status, "lat_ms": r.lat_ms
    } for r in rows])
    

@bp.route("/huellas")
def huellas():
    user = request.args.get("user")
    q = HuellaIP.query
    if user: q = q.filter_by(usuario=user)
    rows = q.order_by(HuellaIP.ultima.desc()).limit(50000).all()
    return jsonify([{
        "usuario": r.usuario, "ip": r.ip,
        "primera_vez": r.primera.isoformat(),
        "ultima_vez": r.ultima.isoformat(), "peticiones": r.peticiones
    } for r in rows])
    
@bp.route("/")
def health(): return {"ok": True}