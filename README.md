# 4202-202514-Grupo3

## ALERTAS

Este proyecto implementa un sistema de generación y gestión de alertas orientado al monitoreo de posibles intrusos en una aplicación. Utiliza Flask, permitiendo el registro de eventos. Además, facilita la auditoría y la visualización de alertas generadas, contribuyendo a la detección temprana eventos.
###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 modelos
 ┃     ┣---- 📜 __init__.py 
 ┃     ┣---- 📜 alertas.py 
 ┣---- 📂 vistas
 ┃     ┣---- 📜 alertas.py 
 ┣---- 📜 .env # Uso local, configuración de variables
 ┣---- 📜 .flaskenv # Uso local, configuración de variables de flask
 ┣---- 📜 .gitignore
 ┣---- 📜 app.py
 ┣---- 📜 extensions.py
 ┣---- 📜 Procfile
 ┣---- 📂 img
       ┣---- 📜 img.png
 ┣---- 📜 README.md
 ┗---- 📜 requirements.txt

```
###  📌 Requisitos

* Intancia docker corriendo, leer README.md de la rama de autorizador
* Python
* pip 
* PostgreSQL (**Si no se hace uso de Dcoker**)

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

`POST /notificar` - Servicio para notificar alertas

Request:
```json
{
    "titulo":"Warning",
    "detalle":"Precaución con el servidor"
}
```

Respuesta:
```json
{
    "id": 3,
    "ok": true
}
```

`GET /alertas` - Servicio para obtener las alertas


Respuesta:
```json
[
    {
        "detalle": "Warning",
        "titulo": "Warning",
        "ts": "2025-09-25T03:46:57.637701"
    },
    {
        "detalle": "Warning",
        "titulo": "Warning",
        "ts": "2025-09-25T03:19:55.112709"
    },
    {
        "detalle": "Prueba detalle",
        "titulo": "Prueba titulo",
        "ts": "2025-09-25T03:12:13.473461"
    }
]
```

`GET /charts/alertas_por_regla.png` - Este servicio retorna una imagen PNG generada dinámicamente con un gráfico de barras que muestra la cantidad de alertas agrupadas por regla (campo titulo). La imagen se envía como respuesta HTTP con el tipo MIME image/png. Si no hay datos, retorna un error 404.


Respuesta:
![img.png](img/img.png)

