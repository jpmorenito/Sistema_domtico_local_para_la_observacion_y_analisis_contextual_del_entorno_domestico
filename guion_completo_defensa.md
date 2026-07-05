# Guion de Defensa del TFG: Sistema Domótico Local e Inteligencia Ambiental

**Diapositivas Totales:** 37 (33 de contenido hablado)
**Duración Objetivo:** 20 minutos (1200 segundos).
**Ritmo:** Tienes una media de 36 segundos por diapositiva. Algunas (como las de arquitectura) requerirán más de 1 minuto, así que pasaremos las introductorias muy rápido.

---

### [0:00 - 0:20] Diapositiva 1: Portada
"Buenos días a los miembros del tribunal, a mi tutor y a los asistentes. Soy Jacob Pino y presento mi Trabajo de Fin de Grado titulado 'Sistema domótico local para la observación y análisis del entorno doméstico'."

### [0:20 - 0:40] Diapositiva 2: Índice de contenidos
"A lo largo de la exposición, abordaré desde la contextualización inicial y los objetivos, hasta llegar a la arquitectura profunda del sistema, el rendimiento obtenido y el análisis de costes y viabilidad, cerrando con una demostración final."

---
## BLOQUE 1: CONTEXTUALIZACIÓN Y OBJETIVOS

### [0:40 - 1:00] Diapositiva 3: Contextualización - Situación Actual
"Empezando por la contextualización, si observamos el ecosistema IoT comercial actual, vemos que nuestras casas están llenas de dispositivos heterogéneos conectados."

### [1:00 - 1:30] Diapositiva 4: Problemas y limitaciones
"Sin embargo, esto presenta tres problemas críticos: primero, la latencia y la dependencia de servidores cloud (las nubes de terceros); segundo, el uso de sensores pasivos como los infrarrojos (PIR) que son reactivos y no inteligentes; y tercero, la falta de privacidad de los datos."

### [1:30 - 1:45] Diapositiva 5: Vamos a darle una solución
"Para resolver esta ineficiencia, en este proyecto se ha propuesto un cambio de paradigma total."

### [1:45 - 2:30] Diapositiva 6: Objetivos principales y específicos
"El objetivo central ha sido diseñar un sistema basado puramente en **Inteligencia Ambiental (AmI)** utilizando hardware de bajo coste. Como objetivos específicos destaco: el diseño de un hardware distribuido, la implementación de telemetría avanzada y la creación de un 'Motor de Contexto' que no solo reaccione, sino que infiera de forma proactiva."

### [2:30 - 3:00] Diapositiva 7: Alcance y limitaciones
"El alcance del prototipo se ha acotado al despliegue de 3 nodos ESP32 con algoritmos de automatización en red local. Como limitaciones iniciales de diseño, asumo restricciones de volumetría del radar y dependencia de la infraestructura eléctrica local."

### [3:00 - 3:30] Diapositiva 8: Solución propuesta
"En resumen, la solución orbita en torno a tres pilares: un funcionamiento 100% local prescindiendo de la nube, la aplicación de *Edge Computing* para procesar los datos en el extremo, y una integración eficiente que nos acerque a la verdadera Inteligencia Ambiental."

---
## BLOQUE 2: ARQUITECTURA DEL HARDWARE

### [3:30 - 4:00] Diapositiva 9: Módulo Ambiente
"Pasando a la arquitectura física, el sistema consta de tres nodos distribuidos. El primero es el Módulo Ambiente, equipado con un sensor DHT11, un fotorresistor LDR, un sensor acústico y el relé de estado sólido que actuará sobre la iluminación."

### [4:00 - 4:30] Diapositiva 10: Módulo Escritorio
"El segundo, y más crítico para la Inteligencia Ambiental, es el Módulo Escritorio. Alberga el radar de ondas milimétricas LD2410 operando por UART y el diodo emisor láser."

### [4:30 - 4:45] Diapositiva 11: Módulo Puerta
"Y finalmente el Módulo Puerta, que cierra el perímetro de seguridad con un sensor magnético Reed."

### [4:45 - 5:15] Diapositiva 12: El Orquestador
"Toda la telemetría generada por estos tres nodos es absorbida por el 'cerebro' del sistema: el Orquestador, alojado en una Raspberry Pi 4 corriendo un entorno Dockerizado."

---
## BLOQUE 3: RED Y COMUNICACIONES

### [5:15 - 5:30] Diapositiva 13: Capa de comunicación
"Para comunicar los nodos con el orquestador, he prescindido de protocolos intermedios."

### [5:30 - 6:30] Diapositiva 14: Topología de red
"Como se ve en este esquema de red, los ESP32 inyectan los datos directamente mediante una API nativa usando **sockets TCP** sobre la red Wi-Fi local al servidor Home Assistant. Para permitir mi acceso seguro desde el exterior sin abrir puertos WAN, he implementado una VPN cifrada *peer-to-peer* mediante Tailscale."

### [6:30 - 7:00] Diapositiva 15: Capa de usuario
"Esto nos permite tener una capa de usuario en forma de Dashboard centralizado y reactivo. Desde aquí puedo supervisar la seguridad y auditar el 'Cerebro de contexto' de forma unificada desde mi teléfono."

### [7:00 - 7:30] Diapositiva 16: Red aislada
"En este esquema lógico se aprecia cómo todo el tráfico está confinado en la red 'Edge'. La frontera exterior está bloqueada, garantizando un aislamiento total contra caídas de proveedores de Internet."

### [7:30 - 8:00] Diapositiva 17: Infraestructura en capas
"A nivel de ingeniería de software, he estructurado el sistema en cuatro capas fuertemente desacopladas: Adquisición física (los ESP32), Transporte (la API TCP), Gestión contextual (Home Assistant) y Persistencia (Base de datos SQLite)."

---
## BLOQUE 4: FLUJO DE DATOS Y MOTOR DE CONTEXTO

### [8:00 - 8:45] Diapositiva 18 y 19: Flujo de inicialización y bucle
*(Pasar de la 18 a la 19 mientras hablas)*
"Al arrancar, los microcontroladores inician sus periféricos, negocian la conexión inalámbrica y establecen el socket TCP. Posteriormente entran en un bucle continuo de muestreo. Serializan la telemetría mediante *Protocol Buffers* y la transmiten, esperando la confirmación o la orden de conmutación desde el servidor."

### [8:45 - 9:30] Diapositiva 20: Flujo API
"Este flujo de ida y vuelta es instantáneo: el nodo envía el estado, Home Assistant procesa la lógica, ordena la conmutación al relé, y de forma paralela registra las series temporales en la base de datos."

### [9:30 - 11:30] Diapositiva 21: Máquina de Estados Contextuales *(¡DEDÍCALE TIEMPO!)*
"Todos estos datos convergen en esta Máquina de Estados Finita, la piedra angular del TFG. El sistema no responde a un solo sensor, sino que hace 'fusión sensorial'. 
Por ejemplo: si la ocupación del radar pasa a 0 durante más de 20 minutos, transiciona automáticamente a 'Ausente'. Si al volver me siento a una distancia corta (Telemetría de estudio), el sistema infiere que estoy en 'Estudio'. 
Pero lo más destacado es el umbral de descanso: si los lúmenes caen a 0 y el radar confirma inmovilidad en la zona de reposo, el sistema cruza ambos datos y transiciona autónomamente de 'Ocio' a 'Durmiendo', sin pulsar ningún botón."

---
## BLOQUE 5: RENDIMIENTO Y RESULTADOS

### [11:30 - 12:30] Diapositiva 22: Rendimiento del sistema
"¿Y cómo se traduce esta arquitectura local en la práctica? En este gráfico podemos ver los resultados empíricos de las pruebas de latencia. Mi sistema consigue tiempos de respuesta de **115 milisegundos**. En comparación con soluciones cloud comerciales como Tuya o Sonoff, que superan los 900 y 1200 ms, mi implementación es entre 8 y 10 veces más rápida."

### [12:30 - 13:15] Diapositivas 23 y 24: Tolerancia a fallos
"Además de ser rápido, el sistema es altamente robusto gracias a dos mecanismos de tolerancia a fallos. 
En primer lugar, a nivel lógico *(Diapositiva 23)*, he implementado una **fusión sensorial redundante** en la Máquina de Estados. Si el radar sufriera un fallo y se quedara 'congelado' indicando falsa presencia, la máquina cuenta con transiciones de guarda por tiempo (como la inactividad superior a 20 minutos) que fuerzan el paso al estado 'Ausente'. Esto garantiza que las luces y actuadores jamás se queden encendidos infinitamente por un bloqueo del hardware.

En segundo lugar, a nivel físico *(pasar a la Diapositiva 24)*, si un nodo sufre una caída de red o de alimentación, el sistema tampoco asume nada a ciegas. Intercepta la pérdida de latidos (heartbeats) del socket TCP y transiciona todas las entidades al estado 'No disponible'. Es un mecanismo 'Fail-Safe' que asegura que, ante la duda, el sistema prioriza la seguridad y desconecta actuadores críticos como el láser."

---
## BLOQUE 6: PRESUPUESTO Y SOSTENIBILIDAD

### [13:00 - 13:45] Diapositiva 25: Consumo energético
"La sostenibilidad operativa ha sido fundamental. Tras medir el régimen continuo de la Raspberry y los 3 nodos, el consumo total del sistema es de apenas **5.15 Vatios**, lo que en términos económicos supone un coste operativo de menos de **10 euros al año** en la factura eléctrica."

### [13:45 - 14:30] Diapositiva 26 y 27: Coste de mantenimiento
*(Pasar de la 26 a la 27)*
"A nivel de despliegue, el coste total del equipamiento hardware es de 124 euros exactos. Al haber utilizado un stack de software 100% de código abierto y dominio público (como Debian, Docker o ESPHome), el coste de licencias es cero. Asumiendo una vida útil de 5 años, el coste de amortización y mantenimiento de la instalación es de **24,80 € al año**."

---
## BLOQUE 7: CONCLUSIÓN Y FUTURO

### [14:30 - 15:15] Diapositiva 28: Objetivos cumplidos
"En conclusión, se ha logrado desarrollar e integrar con éxito un hardware local de adquisición de señales y se ha implementado un motor lógico capaz de dotar a una estancia de verdadera Inteligencia Ambiental, respetando absolutamente la privacidad del usuario."

### [15:15 - 16:15] Diapositiva 29 y 30: Limitaciones encontradas
*(Pasar de la 29 a la 30)*
"Durante el desarrollo también se han identificado limitaciones reales, como el estrés por escritura en la tarjeta SD de la Raspberry (un cuello de botella en sistemas IoT), la sobresaturación inherente de la banda Wi-Fi de 2.4 GHz, y las restricciones de cono de visión que presentan los radares milimétricos."

### [16:15 - 17:15] Diapositiva 31 y 32: Futuras mejoras
*(Pasar de la 31 a la 32)*
"Estas limitaciones marcan mis líneas de trabajo futuro: 
1. La migración del protocolo a redes Mesh Zigbee de ultrabajo consumo.
2. Añadir procesamiento offline de voz mediante la IA de Whisper.
3. Incorporar micro-modelos de Machine Learning (TensorFlow Lite) directamente en los ESP32 para dotarles de inteligencia predictiva.
4. Y desarrollar un acceso por QR efímero en la puerta perimetral."

### [17:15 - 19:45] Diapositiva 33: Demostración del sistema
*(Aquí debes reproducir tu vídeo grabado o hacer una pequeña demo en directo si te lo permiten, comentando cómo se enciende una luz, cómo reacciona el radar, etc.)*

### [19:45 - 20:00] Diapositivas 34 a 37: Bibliografía y Cierre
"En la presentación adjunto las referencias bibliográficas que fundamentan el desarrollo tecnológico y teórico de este trabajo.
Muchas gracias por su atención. Quedo a entera disposición del tribunal para responder a cualquier pregunta técnica que consideren oportuna."
