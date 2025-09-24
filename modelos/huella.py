import datetime
from extensions import db

class HuellaIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), index=True, nullable=False)
    ip = db.Column(db.String(64), index=True, nullable=False)
    primera = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ultima = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    peticiones = db.Column(db.Integer, default=1)
