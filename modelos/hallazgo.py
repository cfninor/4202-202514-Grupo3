import datetime
from extensions import db

class Hallazgo(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    ts_utc = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    regla = db.Column(db.String(120))
    severidad = db.Column(db.String(20))
    total_eventos = db.Column(db.Integer)
    muestra_json = db.Column(db.Text)
