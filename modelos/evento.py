import datetime
from extensions import db

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts_utc = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    ip = db.Column(db.String(64))
    user_agent = db.Column(db.String(256))
    usuario = db.Column(db.String(80))
    rol_reportado = db.Column(db.String(40))
    recurso = db.Column(db.String(80))
    metodo = db.Column(db.String(10))
    token_valido = db.Column(db.Boolean)
    autorizado = db.Column(db.Boolean)
    http_status = db.Column(db.Integer)
    lat_ms = db.Column(db.Integer)
    motivo = db.Column(db.String(120))
