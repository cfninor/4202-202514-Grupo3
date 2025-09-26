# 4202-202514-Grupo3

## AUDITOR

Este proyecto simula un componente **auditor** basado en Flask + JWT.

Es el encargado de registrar todos los eventos recibidos por medio de un microservicio.

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 modelos
 ┃     ┣---- 📜 __init__.py 
 ┃     ┣---- 📜 evento.py 
 ┃     ┣---- 📜 huella.py 
 ┣---- 📂 vistas
 ┃     ┣---- 📜 auditoria.py 
 ┣---- 📜 .env # Uso local, configuración de variables
 ┣---- 📜 .flaskenv # Uso local, configuración de variables de flask
 ┣---- 📜 .gitignore
 ┣---- 📜 app.py
 ┣---- 📜 extensions.py
 ┣---- 📜 Procfile
 ┣---- 📜 README.md
 ┗---- 📜 requirements.txt

```
###  📌 Requisitos

* Intancia docker corriendo, leer README.md de la rama de autorizador
* Python
* pip 
* PostgreSQL (**Si no se hace uso de Docker**)

###  🛠️ Configuración

* **Desde el archivo .env se puede cambiar la configuración de las variables locales y desde .flaskenv las configuraciones de flask**

### 💻 Instalación local

1. Crear un ambiente virtual 
```bash
python -m venv venv              # Instalar venv
# ACTIVAR AMBIENTE
source venv/bin/activate         # Linux/macOS
venv\Scripts\activate            # Windows
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Ejecutar aplicación
```bash
flask run
```
### 🚀 Servicios

`GET /` - Valida el estado del componente

Respuesta:
```json
{
    "ok": true 
}
```

`POST /admin/init` - Crea/inicializa la información en la BD

Respuesta:
```json
{
    "ok": true 
}
```

`POST /log` - Registra el evento en BD

Request:
```json
{
    "usuario": "gerente1",
    "rol": None, 
    "recurso": "login", 
    "metodo": "POST",
    "token_valido": true, 
    "autorizado": true,
    "http_status": 200, 
    "motivo": "login_ok"
}
```

Respuesta:
```json
{
    "ok": true 
}
```

`GET /eventos` - Servicio para devolver el historial de eventos de un usuario

Respuesta:
```json
[
    {
        "autorizado": true,
        "http_status": 200,
        "ip": "127.0.0.1",
        "lat_ms": 0,
        "metodo": "POST",
        "recurso": "login",
        "rol_reportado": null,
        "token_valido": true,
        "ts_utc": "2025-09-23T22:37:47.101135",
        "usuario": "gerente1"
    }
]
```

`GET /huellas` - Servicio para devolver el historial de huellas de un usuario

Respuesta:
```json
[
    {
        "ip": "127.0.0.1",
        "peticiones": 1,
        "primera_vez": "2025-09-23T22:37:47.117713",
        "ultima_vez": "2025-09-23T22:37:47.117719",
        "usuario": "gerente1"
    }
]
```