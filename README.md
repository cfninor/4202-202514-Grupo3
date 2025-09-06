# 4202-202514-Grupo3

## MONITOR

Este proyecto simula un monitor, el cual va a estar revisando el estado de los servicios constantemente.

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 vistas
 ┃     ┣---- 📜 __init__.py
 ┃     ┣---- 📜 estado.py # Variables globales y endpoint para revisar el estado de los servicios
 ┣---- 📜 app.py
 ┣---- 📜 README.md
 ┣---- 📜 Procfile
 ┣---- 📜 requirements.txt
 ┗---- 📜 .gitignore
```

### 🛠️ Configuración

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

3. Variables de entorno (Opcional)
```bash
# WINDOWS
$env:SERVICIOS="http://127.0.0.1:5000,http://127.0.0.1:5001/"
$env:CHECK_INTERVAL_SEC="1.0"
```

4. Ejecutar aplicación
```bash
flask run
```

### 🚀 Servicios
`GET /estado` - Verifica el estado de los servicios

- ✅ Respuesta normal:
```json
{

}
```