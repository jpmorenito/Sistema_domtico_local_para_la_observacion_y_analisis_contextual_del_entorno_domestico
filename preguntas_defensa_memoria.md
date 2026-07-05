# Preguntas de Nivel Avanzado (Basadas en la Memoria del TFG)

He leído a fondo tu documento de memoria (capítulos 3, 4, 5 y 7). Aquí tienes preguntas "con veneno" que un tribunal exigente podría sacarte tras leer tu texto, con sus respectivas respuestas preparadas.

---

## 1. Sobre la Selección de Tecnologías (Capítulo 5)

> **Pregunta:** *"En la Tabla comparativa 5.1 de su memoria, menciona que la Orange Pi 5 Plus tiene una unidad NPU de 6 TOPS dedicada para Inteligencia Artificial. Sin embargo, elige la Raspberry Pi 4 de solo 1GB de RAM. ¿No habría sido mucho mejor usar la Orange Pi para procesar los vectores del radar de forma más inteligente?"*
**Respuesta:** Desde un punto de vista puramente computacional, sí. Pero desde el punto de vista de la ingeniería domótica, no. Como detallo en la sección 5.2.1, la decisión prioriza el **consumo energético**. La Orange Pi tiene picos de consumo altísimos (hasta 12W+) y un soporte de software fragmentado. Al usar Edge Computing básico (algoritmos condicionales en lugar de Redes Neuronales pesadas), 1 GB de RAM es más que suficiente (Home Assistant solo consume unos 620 MB estables), permitiéndome además usar un Sistema de Alimentación Ininterrumpida (SAI) mucho más pequeño y barato, cumpliendo así con los requisitos no funcionales de eficiencia.

> **Pregunta:** *"En la sección de comunicaciones habla de usar la 'API nativa de ESPHome sobre sockets TCP'. ¿Por qué descartó el uso de MQTT, que es el protocolo estándar de facto en la industria del Internet de las Cosas?"*
**Respuesta:** MQTT es excelente para despliegues a gran escala y redes inestables gracias a su patrón de publicación/suscripción. Sin embargo, en la arquitectura de mi TFG (una red local cableada/Wi-Fi aislada de internet), introducir un broker MQTT (como Mosquitto) añadía un intermediario innecesario. La API nativa TCP de ESPHome establece un túnel directo *punto a punto* entre el nodo y Home Assistant, reduciendo el *overhead* de red y permitiendo esas latencias ultrabajas de 115 milisegundos que documento en el Capítulo 7.

---

## 2. Sobre Pruebas Funcionales (Capítulo 7)

> **Pregunta:** *"En la página de validación de pruebas menciona el uso del 'Motor de trazas de ejecución' (Automation Traces) de Home Assistant. ¿Cómo nos garantiza científicamente que esos tiempos de latencia de 115ms no son una casualidad o están falseados?"*
**Respuesta:** El motor de trazas de Home Assistant no es una simple representación gráfica, es un auditor interno que guarda archivos en formato estructurado JSON. En ese JSON se estampa un *Timestamp* a nivel de kernel cada vez que se evalúa un bloque lógico (Trigger $\rightarrow$ Condition $\rightarrow$ Action). La medición de 115 ms no es una apreciación humana, sino la resta matemática entre el timestamp en el que el servidor recibió el paquete del ESP32 y el timestamp en el que ejecutó el comando sobre el relé.

---

## 3. Sobre Casos de Uso y Máquina de Estados (Capítulo 4)

> **Pregunta:** *"En la sección de tolerancia a fallos menciona la 'Fusión sensorial redundante'. ¿Qué ocurre matemáticamente en la máquina de estados si, por ejemplo, el radar y el sensor de luz entran en conflicto dando datos contradictorios continuamente?"*
**Respuesta:** La máquina de estados está programada con **condiciones de guarda jerárquicas**. Si dos sensores entran en conflicto, el sistema no entra en un bucle infinito encendiendo y apagando luces (efecto *flickering*). Se prioriza la seguridad y la inactividad. He configurado retardos de histéresis (tiempos mínimos de permanencia en un estado) para absorber esas contradicciones transitorias, y ante un fallo sostenido que vulnere las reglas, las automatizaciones tienen un *timeout* (tiempo de expiración) que devuelve el sistema a un estado de reposo ('Ocio' o 'Ausente').

> **Pregunta:** *"Su Caso de Uso 3 define el 'Pomodoro espacial', parpadeando la luz general a los 50 minutos ininterrumpidos. Si yo soy un programador o estudiante cuyo umbral de concentración es de 2 horas continuas, ¿su sistema me va a cortar la concentración obligatoriamente parpadeándome la luz?"*
**Respuesta:** Excelente apreciación. La Inteligencia Ambiental busca el bienestar, no la intrusión. Por diseño, los parámetros de los tiempos (como esos 50 minutos) no están codificados en duro (*hardcoded*) en el código fuente (C++). Son variables de entrada (Inputs numéricos) definidas en el panel de control de Home Assistant. El usuario administrador puede deslizar una barra en el dashboard móvil para cambiar ese umbral de 50 minutos a 120 minutos, o desactivar la automatización por completo con un simple *switch* virtual, haciendo el sistema totalmente adaptable a las necesidades de cada persona.
