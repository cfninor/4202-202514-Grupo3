import datetime
from extensions import db

class Alerta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts_utc = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    titulo = db.Column(db.String(160))
    detalle_json = db.Column(db.Text)
    entregado = db.Column(db.Boolean, default=False)
