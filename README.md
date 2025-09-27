# 4202-202514-Grupo3

* Este repositorio contiene cada componente por rama.

### main
Rama principal que contiene la documentación, instrucciones generales y lineamientos de los experimentos asociados a la disponibilidad y seguridad.

## Ejecución en Heroku

Cada servicio está desplegado en **Heroku** y puede ser probado mediante la colección de **Postman** incluida en el proyecto (`4202-Arquitectura.postman_collection.json`).

# Experimento - Seguridad
## Propósito del experimento
Este experimento busca detectar posibles intrusiones o comportamientos anómalos en una plataforma de microservicios desarrollada con Python y Flask. La arquitectura está compuesta por cinco servicios desplegables, conectados a una base de datos PostgreSQL.

El objetivo de este experimento es simular un sistema que:

- Autentica usuarios con roles asociados.
- Audita accesos y acciones en el sistema.
- Detecta intrusiones mediante análisis de IP, horarios inusuales o accesos simultáneos desde diferentes ubicaciones.
- Emite alertas ante eventos anómalos.
---

## Estructura de ramas

### autorizador
- Autenticación con usuario y contraseña (bcrypt).
- Emisión de tokens JWT.
- Validación de roles por recurso.
- Registra los logins exitosos y fallidos en el `auditor`.

### auditor
- Guarda cada intento de acceso (login, peticiones a servicios).
- Almacena IP, usuario, recurso y hora.
- Actúa como fuente de datos para el detector.

### deteccion
- Analiza logs desde el `auditor`.
- Detecta eventos como:
  - Accesos en horarios inusuales para el usuario.
  - Cambios de IP repentinos.
  - Accesos a recursos con roles incorrectos.
  - Accesos simultáneos desde diferentes IPs.
- Usa `pandas` para análisis y gráficos.

### alertas
- Recibe alertas desde el detector.
- Las almacena para revisión posterior.
- Permite consultar las alertas detectadas.

### historial
- Expone un endpoint protegido por autorización.
- Devuelve información de historial de compra del usuario.

# Experimento - Disponibilidad

## Propósito del experimento

Este proyecto implementa y valida un diseño de **redundancia activa** para un servicio de consulta de pedidos.  
El objetivo es demostrar que, mediante **balanceo de carga** y **monitoreo con heartbeat**, el sistema puede enmascarar la falla de una instancia y mantener la disponibilidad del servicio para el usuario final, incluso ante caídas.

---

## Estructura de ramas

### ms-pedidos
- Microservicio desarrollado en **Flask (Python)** para la consulta de pedidos.  
- Expone endpoints de **estado**, **salud** y **consulta de pedidos**.  
- Permite simular caídas controladas y variaciones de latencia.  

### balanceador
- Servicio de **balanceo de carga** en **Flask/Python con NGINX**.  
- Distribuye solicitudes entre las instancias activas.  
- Retira del pool aquellas que fallen según la información del monitor.  

### monitor
- Servicio de **heartbeat** que valida periódicamente la disponibilidad de cada instancia de `ms-pedidos`.  
- Expone un endpoint `/estado` para consultar la salud de los servicios.  
- Notifica al balanceador para mantener actualizado el conjunto de instancias activas.  
