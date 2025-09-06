# 4202-202514-Grupo3

## MS-PEDIDOS

Este proyecto simula una API de pedidos con latencias artificiales y también expone un servicio para poder simular caídas lógicas.

###  📁 Estructura del Proyecto

```
📦 root
 ┣---- 📂 vistas
 ┃     ┣---- 📜 __init__.py
 ┃     ┣---- 📜 estado.py # Variables globales y endpoint para poder simular caída o levantar el servicio
 ┃     ┣---- 📜 pedido.py # Endpoint para consultar un pedido
 ┃     ┣---- 📜 salud.py # Endpoint para consultar el estado del servicio (Health check)
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
$env:INSTANCE_NAME="ms-pedido-1"
$env:LAT_MS="120"
```

4. Ejecutar aplicación
```bash
flask run
```

### 🚀 Servicios
`GET /salud` - Verifica el estado lógico de la instancia.

- ✅ Respuesta normal:
```json
{
  "instancia": "ms-pedido-1",
  "estado": "FUNCIONANDO"
}
```

- ❌ Si está en modo caída:
```json
{
  "instancia": "ms-pedido-1",
  "estado": "CAIDO"
}
```

---

`GET /estado?on=true|false` - Activa o desactiva el modo "caída lógica" de la instancia.

- Ejemplo:
```
/estado?on=true   # activa la caída
/estado?on=false  # vuelve a modo normal
```

Respuesta:
```json
{
  "instancia": "ms-pedido-1",
  "caida": true
}
```

---

`GET /pedido/<id_pedido>` - Devuelve el estado aleatorio de un pedido, simulando latencia artificial.

- ✅ Si la instancia está activa:
```json
{
  "instancia": "ms-pedido-1",
  "pedidoId": "<id_pedido>",
  "estado": "ENVIADO"
}
```

- ❌ Si la instancia está caída:
```json
{
  "instancia": "ms-pedido-1",
  "error": "instancia caida"
}
```