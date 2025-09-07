# 4202-202514-Grupo3

**Propósito del experimento**

Este proyecto implementa y valida un diseño de redundancia activa para un servicio de consulta de pedidos. El objetivo es demostrar que, mediante balanceo de carga y monitoreo con heartbeat, el sistema puede enmascarar la falla de una instancia y mantener la disponibilidad del servicio para el usuario final, incluso ante caídas.

Se realizaron pruebas automatizadas con Postman, incluyendo 61 iteraciones y 122 tests, que permitieron analizar la disponibilidad, la latencia y el comportamiento del balanceador al retirar y reincorporar instancias.


**Estructura de ramas**

    main
    
Rama principal que contiene la documentación, instrucciones generales y lineamientos del experimento.

    ms-pedidos

  Contiene el microservicio desarrollado en Flask (Python) para la consulta de pedidos.
  
  Expone endpoints de estado, salud y consulta de pedidos.
  
  Permite simular caídas controladas y variaciones de latencia.

    balanceador

  Implementa el servicio de balanceo de carga en Flask/Python con NGINX, encargado de distribuir las solicitudes entre las instancias activas y retirar del pool aquellas que fallen.
  monitor
  
  Servicio encargado del heartbeat. Revisa periódicamente la salud de cada instancia de ms-pedidos y notifica al balanceador para mantener actualizado el estado de los backends.
  test
  
  Rama auxiliar utilizada para validar los servicios y realizar pruebas de integración con la colección de Postman y las configuraciones en Heroku.

  
**Ejecución en Heroku**

Cada servicio está desplegado en Heroku y puede ser probado a través de la colección de Postman incluida en el proyecto.
