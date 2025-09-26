from flask import Flask
from dotenv import load_dotenv
from vistas.historial import bp as autorizacion_bp

load_dotenv()
app = Flask(__name__)

app.register_blueprint(autorizacion_bp)