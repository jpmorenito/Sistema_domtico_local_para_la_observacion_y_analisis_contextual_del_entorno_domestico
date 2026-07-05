# Posibles Preguntas del Tribunal y Respuestas Recomendadas

A los tribunales de ingeniería les gusta poner a prueba tu conocimiento preguntándote "por qué" tomaste ciertas decisiones en lugar de usar otras tecnologías comerciales, o buscando puntos débiles en tu sistema. Aquí tienes las más probables y cómo responderlas con seguridad.

---

## 1. Sobre Arquitectura y Hardware

> **Pregunta:** *"¿Por qué ha decidido usar Home Assistant en una Raspberry Pi en lugar de una solución comercial en la nube como Alexa, Google Home o Tuya, que son más fáciles de instalar?"*
**Respuesta:** Por tres motivos fundamentales: **Latencia, Privacidad y Resiliencia**. Como demuestro en la gráfica de rendimiento de mi memoria, un sistema cloud tiene latencias de más de 1000 ms, mientras que mi arquitectura local (Edge Computing) responde en 115 ms. Además, garantizo la privacidad total del usuario al no enviar telemetría a servidores externos, y el sistema sigue funcionando perfectamente aunque se caiga la conexión a internet del proveedor.

> **Pregunta:** *"¿Por qué eligió usar ESPHome y no programar los ESP32 desde cero usando C++ o FreeRTOS?"*
**Respuesta:** Por eficiencia en la ingeniería del software y escalabilidad. ESPHome genera internamente un código C++ altamente optimizado y compilado. Me permitió abstraer la capa de hardware y centrarme en el diseño lógico (la Máquina de Estados). Además, implementa de forma nativa mecanismos críticos como reconexiones seguras y latidos (heartbeats) por TCP, lo que reduce la deuda técnica del proyecto.

---

## 2. Sobre Inteligencia Ambiental (AmI)

> **Pregunta:** *"En su título menciona 'Inteligencia Ambiental'. ¿Qué diferencia exacta hay entre su proyecto y simplemente encender una luz desde el móvil?"*
**Respuesta:** La diferencia radica en la **proactividad y el contexto**. Encender una luz con el móvil es domótica clásica reactiva (el usuario da una orden explícita). Mi sistema aplica Inteligencia Ambiental porque *infiere* el estado del usuario sin que este interactúe. Gracias a la Fusión Sensorial (cruzar datos del radar, luz y tiempo), el sistema sabe si estoy estudiando o durmiendo, y actúa en consecuencia de forma invisible.

> **Pregunta:** *"¿Qué pasaría si el radar detecta movimiento pero el sensor de luz (LDR) falla y dice que hay luz de día cuando es de noche?"*
**Respuesta:** Para eso he diseñado la Máquina de Estados Contextuales. El sistema depende de la fusión de múltiples sensores. Si el LDR fallase bloqueándose en un valor de alta luminosidad, el sistema no transicionaría al estado 'Durmiendo', manteniéndose en estado seguro. Como mejora futura he planteado añadir redundancia física (dos sensores) para hacer un sistema de votación mayoritaria ante estos casos.

---

## 3. Sobre Redes y Seguridad

> **Pregunta:** *"Si todo está en red local, ¿cómo accede desde fuera de su casa para ver el dashboard sin comprometer la seguridad abriendo puertos en el router?"*
**Respuesta:** He implementado una VPN *peer-to-peer* basada en WireGuard mediante Tailscale. Esto crea un túnel cifrado extremo a extremo entre mi móvil y la Raspberry Pi, sin necesidad de abrir ningún puerto en el firewall del router, mitigando el riesgo de ataques automatizados desde la red pública (WAN).

> **Pregunta:** *"¿El tráfico Wi-Fi entre los ESP32 y la Raspberry Pi va en claro? ¿Podría alguien interceptar esa telemetría dentro de casa?"*
**Respuesta:** No, la API nativa de ESPHome implementa la capa de cifrado *Noise Protocol Framework*. Todos los paquetes TCP que viajan por el aire están cifrados, por lo que incluso si alguien lograra descifrar el tráfico de la red Wi-Fi (WPA3), solo vería paquetes binarios ininteligibles entre el nodo y el servidor.

---

## 4. Sobre Problemas y Limitaciones

> **Pregunta:** *"Menciona en sus diapositivas el desgaste de la tarjeta SD de la Raspberry Pi. Si este proyecto se vendiera a un cliente, ¿se le rompería el sistema en unos meses?"*
**Respuesta:** Efectivamente, las bases de datos de series temporales (como el Recorder de Home Assistant) implican escrituras constantes que degradan rápidamente la memoria flash de una tarjeta MicroSD. En el contexto de este prototipo académico es asumible, pero en un entorno de producción, la solución estándar, que ya contempla el software, es conectar un disco duro de estado sólido (SSD) externo por USB a la Raspberry Pi o externalizar la base de datos a un NAS.

> **Pregunta:** *"¿Por qué la banda de 2.4 GHz es una limitación para su proyecto?"*
**Respuesta:** Porque el espectro de 2.4 GHz está altamente saturado en entornos urbanos (Bluetooth, Wi-Fi de vecinos, microondas). Aunque el ESP32 solo es compatible con 2.4 GHz y actualmente funciona bien gracias al filtrado local que reduce los paquetes, en instalaciones más grandes (decenas de nodos) el ruido espectral provocaría pérdida de paquetes. Por ello propongo en las futuras mejoras migrar la sensórica a redes de malla Zigbee o Thread.

---

## 5. El "Comodín" (Si te quedas en blanco o no sabes algo)

Si te preguntan algo técnico que realmente no has implementado o no sabes responder exactamente, **nunca mientas ni divagues**. Usa esta estructura profesional:

> *"Ese es un punto muy interesante. Durante la delimitación del alcance del proyecto (scope), decidí priorizar [lo que sí has hecho, ej: el desarrollo local], por lo que ese aspecto específico quedó fuera de la iteración actual del prototipo. Sin embargo, su propuesta encaja perfectamente dentro de mi hoja de ruta de futuras mejoras, ya que se podría integrar aplicando [breve idea de cómo lo harías]."*
