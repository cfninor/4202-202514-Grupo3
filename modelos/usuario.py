import datetime
from extensions import db

class Usuario(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    zona_horaria = db.Column(db.String(40), default="UTC")
    creado = db.Column(db.DateTime, default=datetime.datetime.utcnow)