# 4202-202514-Grupo3

## ALERTAS

Este proyecto simula un **autenticador/autorizador** basado en Flask + JWT.

Permite hacer el login, control de acceso por rol y generar auditoria del inicio de sesión.

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 modelos
 ┃     ┣---- 📜 __init__.py 
 ┃     ┣---- 📜 recurso.py 
 ┃     ┣---- 📜 rol.py 
 ┃     ┣---- 📜 usuario_rol.py 
 ┃     ┣---- 📜 usuario.py 
 ┣---- 📂 vistas
 ┃     ┣---- 📜 autorizacion.py 
 ┣---- 📜 .env # Uso local, configuración de variables
 ┣---- 📜 .flaskenv # Uso local, configuración de variables de flask
 ┣---- 📜 .gitignore
 ┣---- 📜 app.py
 ┣---- 📜 docker-compose.yml # Docker postgres
 ┣---- 📜 extensions.py
 ┣---- 📜 Procfile
 ┣---- 📜 README.md
 ┗---- 📜 requirements.txt

```
###  📌 Requisitos

* Docker instalado
* Python
* pip 
* PostgreSQL (**Si no se hace uso de Dcoker**)

###  🛠️ Configuración

* **Desde el archivo docker-compose.yml se puede cambiar la configuración para Docker.**
* **Desde el archivo .env se puede cambiar la configuración de las variables locales y desde .flaskenv las configuraciones de flask**

### 🐳 Uso con Docker

1. Levantar la base de datos
```bash
docker compose up -d
```

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

`POST /login` - Servicio para iniciar sesión

Request:
```json
{
    "usuario": "gerente1",
    "contrasena": "Passw0rd!"
}
```

Respuesta:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnZXJlbnRlMSIsInJvbCI6ImNvbWVyY2lhbCIsImlhdCI6MTc1ODU5ODkxOSwiZXhwIjoxNzU4NjAwNzE5fQ.Nx7qx22CFt5SGQ6q1SLylCBnFU4mNDQ_-5JySJuEuWk",
    "rol": "comercial",
    "roles": [
        "comercial"
    ]
}
```

`POST /verificar` - Servicio para validar el rol

Request:
```json
{
    "usuario": "gerente1",
    "rol": "comercial"
}
```

Respuesta:
```json
{
    "autorizado": true,
    "rol_requerido": "comercial"
}
```