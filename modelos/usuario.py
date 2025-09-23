import datetime
from extensions import db

class Usuario(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    zona_horaria = db.Column(db.String(40), default="UTC")
    creado = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    intentos_fallidos = db.Column(db.Integer, default=0)
    bloqueo_hasta = db.Column(db.DateTime, nullable=True)
    ultimo_login = db.Column(db.DateTime, nullable=True)