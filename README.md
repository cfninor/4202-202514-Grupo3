# 4202-202514-Grupo3

## BALANCEADOR

Este proyecto simula un balanceador entre los servicios.

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 vistas
 ┃     ┣---- 📜 __init__.py
 ┃     ┣---- 📜 balanceador.py # Variables globales, servicio de pedidos y estado
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
$env:HEARTBEAT_URL="http://127.0.0.1:5001/estado"
$env:BACKEND_TIMEOUT="1.2"
$env:FLASK_RUN_PORT=5002 # Puerto diferente al de los servicios y al del monitor
```

4. Ejecutar aplicación
```bash
flask run
```

### 🚀 Servicios

`GET /estado` - Valida el estado de los servicios

Respuesta:
```json
{
    "healthy_backends": [
        "http://127.0.0.1:5000"
    ],
    "snapshot": {
        "http://127.0.0.1:5000": {
            "healthy": true
        }
    },
    "recent": [
        {
            "t": 1757132618.4226427,
            "target": "http://127.0.0.1:5000",
            "result": 200
        },
        {
            "t": 1757132631.787409,
            "target": "http://127.0.0.1:5000",
            "result": 200
        }
    ]
}
```

---

`GET /pedido/<id_pedido>` - Devuelve el pedido

- ✅ Si la instancia está activa:
```json
{
  "instancia": "ms-pedido-1",
  "pedidoId": "<id_pedido>",
  "estado": "ENVIADO"
}
```