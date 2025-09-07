# 4202-202514-Grupo3

## Propósito del experimento

Este proyecto implementa y valida un diseño de **redundancia activa** para un servicio de consulta de pedidos.  
El objetivo es demostrar que, mediante **balanceo de carga** y **monitoreo con heartbeat**, el sistema puede enmascarar la falla de una instancia y mantener la disponibilidad del servicio para el usuario final, incluso ante caídas.

---

## Estructura de ramas

### main
Rama principal que contiene la documentación, instrucciones generales y lineamientos del experimento.

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

### test
- Rama auxiliar utilizada para validar los servicios.  
- Contiene pruebas de integración realizadas con la colección de **Postman** y configuraciones de despliegue en **Heroku**.  

---

## Ejecución en Heroku

Cada servicio está desplegado en **Heroku** y puede ser probado mediante la colección de **Postman** incluida en el proyecto (`4202-Arquitectura.postman_collection.json`).
