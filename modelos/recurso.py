from extensions import db

class Recurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recurso = db.Column(db.String(120), nullable=False)
    rol_requerido = db.Column(db.String(40), nullable=False)
