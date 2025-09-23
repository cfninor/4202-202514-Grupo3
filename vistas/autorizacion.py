import os, datetime, jwt, requests
from passlib.hash import bcrypt
from flask import Blueprint, request, jsonify, abort
from extensions import db
from modelos import Usuario, Rol, Recurso, UsuarioRol

bp = Blueprint("autorizacion", __name__)
ADMIN_SECRET = os.getenv("ADMIN_SECRET","autorizador-admin-secret")
JWT_SECRET   = os.getenv("JWT_SECRET","jwt-secret")
AUDITOR_LOG_URL = os.getenv("AUDITOR_LOG_URL")

INTENTOS_BLOQUEAR = 5
MINUTOS_BLOQUEAR = 10

def _client_ip(req):
    return req.headers.get("X-Forwarded-For", req.remote_addr) or "0.0.0.0"

def audit_login(req, usuario, exito, motivo=""):
    if not AUDITOR_LOG_URL: return
    try:
        requests.post(
            AUDITOR_LOG_URL,
            json={
                "usuario": usuario, "rol": None, "recurso": "login", "metodo": "POST",
                "token_valido": exito, "autorizado": exito,
                "http_status": 200 if exito else 401, "motivo": motivo
            },
            headers={"X-Forwarded-For": _client_ip(req)},
            timeout=2
        )
    except Exception:
        pass
    
@bp.route("/admin/init", methods=["POST"])
def admin_init():
    if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
    db.create_all()
    if not Rol.query.first():
        db.session.add_all([Rol(nombre="comercial"), Rol(nombre="logistica")]); db.session.commit()
    if not Usuario.query.filter_by(usuario="gerente1").first():
        g1 = Usuario(usuario="gerente1", zona_horaria="America/Bogota", contrasena=bcrypt.hash("Passw0rd!"))
        g2  = Usuario(usuario="gerente2",  zona_horaria="America/Bogota", contrasena=bcrypt.hash("Passw0rd!"))
        db.session.add_all([g1, g2]); db.session.commit()
        rcom = Rol.query.filter_by(nombre="comercial").first().id
        rlog = Rol.query.filter_by(nombre="logistica").first().id
        db.session.add_all([UsuarioRol(usuario_id=g1.id, rol_id=rcom),
                            UsuarioRol(usuario_id=g2.id,  rol_id=rlog)])
        if not Recurso.query.first():
            db.session.add(Recurso(recurso="historial", rol_requerido="comercial"))
        db.session.commit()
    return {"ok": True}

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    usuario, contrasena = (data.get("usuario") or "").strip(), (data.get("contrasena") or "")
    u = Usuario.query.filter_by(usuario=usuario).first()
    if not u:
        audit_login(request, usuario, False, "usuario_inexistente")
        return jsonify({"error":"Credenciales inválidas"}), 401
    now = datetime.datetime.now(datetime.timezone.utc)
    if u.bloqueo_hasta and now < u.bloqueo_hasta:
        audit_login(request, usuario, False, "usuario_bloqueado")
        return jsonify({"error":"Usuario bloqueado temporalmente"}), 423
    if not bcrypt.verify(contrasena, u.contrasena):
        u.intentos_fallidos = (u.intentos_fallidos or 0)+1
        if u.intentos_fallidos >= INTENTOS_BLOQUEAR:
            u.bloqueo_hasta = now + datetime.timedelta(minutes=MINUTOS_BLOQUEAR)
            u.intentos_fallidos = 0
        db.session.commit()
        audit_login(request, usuario, False, "password_incorrecto")
        return jsonify({"error":"Credenciales inválidas"}), 401

    u.intentos_fallidos, u.bloqueo_hasta, u.ultimo_login = 0, None, now
    db.session.commit()

    roles_usuario = {
        r[0] for r in db.session.query(Rol.nombre)
        .join(UsuarioRol, Rol.id==UsuarioRol.rol_id)
        .join(Usuario, Usuario.id==UsuarioRol.usuario_id)
        .filter(Usuario.usuario==usuario).all()
    }
    rol_principal = sorted(roles_usuario)[0] if roles_usuario else "user"
    token = jwt.encode({
        "sub": usuario, "rol": rol_principal,
        "iat": int(now.timestamp()), "exp": int((now+datetime.timedelta(minutes=30)).timestamp())
    }, JWT_SECRET, algorithm="HS256")

    audit_login(request, usuario, True, "login_ok")
    return jsonify({"access_token": token, "rol": rol_principal, "roles": list(roles_usuario)}), 200

@bp.route("/verificar", methods=["POST"])
def verificar():
    data = request.get_json(force=True)
    usuario, rol_reportado = data["usuario"], data.get("rol")
    recurso = data.get("recurso", "historial")
    roles_usuario = {
        r[0] for r in db.session.query(Rol.nombre)
        .join(UsuarioRol, Rol.id==UsuarioRol.rol_id)
        .join(Usuario, Usuario.id==UsuarioRol.usuario_id)
        .filter(Usuario.usuario==usuario).all()
    }
    pol = Recurso.query.filter_by(recurso=recurso).first()
    requerido = pol.rol_requerido if pol else None
    autorizado = (requerido in roles_usuario) and (rol_reportado in roles_usuario)
    return jsonify({"autorizado": autorizado, "rol_requerido": requerido}), (200 if autorizado else 403)

@bp.route("/")
def health(): return {"ok": True}