# 4202-202514-Grupo3

## HISTORIAL

Este proyecto simula un servicio de **Historial**,  basado en Flask + JWT.

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 vistas
 ┃     ┣---- 📜 historial.py 
 ┣---- 📜 .env # Uso local, configuración de variables
 ┣---- 📜 .flaskenv # Uso local, configuración de variables de flask
 ┣---- 📜 .gitignore
 ┣---- 📜 app.py
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

`GET /historial/<usuario>` - Servicio para consultar el historial

Respuesta:
```json
{
    "historial":[
        "pedido-001",
        "pedido-002"
    ]
}
```