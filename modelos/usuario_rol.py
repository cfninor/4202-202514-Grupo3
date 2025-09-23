from extensions import db

class UsuarioRol(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
