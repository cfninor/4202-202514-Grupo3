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

`POST /reglas` - 

Request:
```json

```

Respuesta:
```json

```

`GET /reglas` - 

Respuesta:
```json

```