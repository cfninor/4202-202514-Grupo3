# 4202-202514-Grupo3

## DETECCIÓN

Este proyecto simula un **detector de anomalias** basado en Flask.

Los eventos a detectar son:
* Rol no pertenece al usuario
* Transacciones fuera de horario
* Transacciones muy seguidas (Rate por minuto)
* El uso de una IP nueva
* Varias IP's para el mismo usuario en poco tiempo
* Concurrencia del mismo usuario en diferentes IP's

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 modelos
 ┃     ┣---- 📜 __init__.py 
 ┃     ┣---- 📜 hallazgo.py 
 ┃     ┣---- 📜 usuario.py 
 ┣---- 📂 vistas
 ┃     ┣---- 📜 detector.py 
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

`POST /reglas` - Modifica las reglas en el sistema

Request:
```json
{
    "IP_DIAS_VIGENTES": 30,
    "IP_DIVERSIDAD_UMBRAL": 5,
    "corroboracion_minima": 1,
    "fuera_horario": {
        "fin": 22,
        "inicio": 6
    },
    "rate_por_min": {
        "ip": 60,
        "usuario": 30
    }
}
```

Respuesta:
```json
{
    "IP_DIAS_VIGENTES": 30,
    "IP_DIVERSIDAD_UMBRAL": 5,
    "corroboracion_minima": 1,
    "fuera_horario": {
        "fin": 22,
        "inicio": 6
    },
    "rate_por_min": {
        "ip": 60,
        "usuario": 30
    }
}
```

`GET /reglas` - Devuelve las reglas configuradas

Respuesta:
```json
{
    "IP_DIAS_VIGENTES": 30,
    "IP_DIVERSIDAD_UMBRAL": 5,
    "corroboracion_minima": 1,
    "fuera_horario": {
        "fin": 22,
        "inicio": 6
    },
    "rate_por_min": {
        "ip": 60,
        "usuario": 30
    }
}
```

`POST /admin/start` - Inicia servicio de validación y detección de eventos

Respuesta:
```json
{
    "running": true
}
```

`POST /admin/stop` - Finaliza servicio de validación y detección de eventos

Respuesta:
```json
{
    "running": false
}
```