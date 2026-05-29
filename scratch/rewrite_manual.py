import os

tex_content = r"""\newpage
\section{Manual de Usuario}
\label{anexo:manual_usuario}

El presente manual proporciona una guía detallada y estructurada para la puesta en marcha, configuración y uso diario del sistema domótico local. Está diseñado para servir tanto al administrador del sistema (encargado del despliegue en el servidor) como al usuario final (residente de la habitación).

\subsection{Introducción}
El sistema domótico está basado en una arquitectura cliente-servidor de forma completamente local. Utiliza una \textbf{Raspberry Pi 4} como servidor central y placas \textbf{ESP32} como nodos sensores repartidos por la estancia. Para interactuar con el sistema, se dispone de un panel de control accesible vía web o mediante aplicación móvil.

\subsection{Requisitos Previos}
Para la correcta implementación de este proyecto, es imprescindible contar con los siguientes elementos:

\subsubsection{Requisitos de Hardware}
\begin{itemize}
    \item Servidor central: \textbf{Raspberry Pi 4} (se recomienda modelo de 4GB u 8GB de RAM), con fuente de alimentación oficial de $5.1\,\text{V}/3.0\,\text{A}$ y una tarjeta microSD de al menos 32GB (clase 10 o superior).
    \item Nodos sensores: Placas de desarrollo \textbf{ESP32} genéricas.
    \item Componentes periféricos: Sensores (Radar mmWave, DHT11, Relé, Contacto Magnético, LDR, Micrófono KY-037, Láser) y cableado Dupont.
    \item Enrutador (router) doméstico con conexión a internet y puertos Ethernet disponibles.
\end{itemize}

\subsubsection{Requisitos de Software}
\begin{itemize}
    \item Sistema operativo del servidor: \textbf{Raspberry Pi OS} (versión de 64 bits recomendada).
    \item Plataforma de virtualización: \textbf{Docker} y opcionalmente el gestor visual \textbf{Portainer}.
    \item Servicios núcleo: \textbf{Home Assistant} y \textbf{ESPHome}.
    \item Acceso remoto seguro: \textbf{Tailscale} (VPN).
\end{itemize}

\subsection{Configuración e Inicialización del Servidor Central}
A continuación, se detalla el proceso técnico, paso por paso, para instalar la infraestructura de software necesaria en la Raspberry Pi y levantar los servicios que orquestan la inteligencia de la habitación.

\subsubsection{1. Instalación de Docker}
Con la Raspberry Pi conectada a la red e iniciado el sistema operativo Raspberry Pi OS, abre un terminal (ya sea físicamente o mediante SSH) e introduce el comando oficial de instalación de Docker:
\begin{verbatim}
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
\end{verbatim}
Para evitar usar \texttt{sudo} en cada ejecución de Docker, añade tu usuario actual (por ejemplo, \texttt{jpmorenito} o \texttt{pi}) al grupo \texttt{docker}:
\begin{verbatim}
sudo usermod -aG docker $USER
\end{verbatim}

\subsubsection{2. Despliegue de Servicios mediante Docker}
El sistema se compone de tres contenedores principales que deben ejecutarse en la Raspberry Pi.

\textbf{Paso 1: Iniciar Portainer (Gestor visual de contenedores)}
Portainer permite administrar Docker desde una interfaz web gráfica de forma intuitiva.
\begin{verbatim}
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:latest
\end{verbatim}

\textbf{Paso 2: Iniciar Home Assistant (Cerebro domótico)}
Utiliza la red del servidor anfitrión (\texttt{--network=host}) para detectar dispositivos de la red local de forma automática.
\begin{verbatim}
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Europe/Madrid \
  -v /home/jpmorenito/homeassistant:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
\end{verbatim}

\textbf{Paso 3: Iniciar ESPHome (Programador de nodos)}
Este servicio se encarga de compilar y transmitir el código a las placas ESP32 de los nodos de la habitación.
\begin{verbatim}
docker run -d \
  --name esphome \
  --restart=always \
  -e TZ=Europe/Madrid \
  -v /opt/esphome/config:/config \
  -v /etc/localtime:/etc/localtime:ro \
  --network=host \
  ghcr.io/esphome/esphome
\end{verbatim}

\subsubsection{3. Acceso Remoto Seguro (VPN con Tailscale)}
Para permitir el acceso a Home Assistant desde fuera de casa sin abrir puertos en el router (lo cual compromete la seguridad), se utiliza Tailscale.
\begin{enumerate}
    \item Instala Tailscale en la Raspberry Pi ejecutando: \texttt{curl -fsSL https://tailscale.com/install.sh | sh}
    \item Inicia el servicio y actívalo con: \texttt{sudo tailscale up}
    \item Aparecerá un enlace de autenticación en la pantalla. Ábrelo en un navegador para vincular la Raspberry Pi a tu cuenta gratuita de Tailscale. A partir de este momento, la Raspberry Pi tendrá asignada una IP privada segura (por ejemplo, \texttt{100.x.x.x}).
\end{enumerate}

\subsection{Manual del Dispositivo (Hardware y Ubicación)}
El sistema físico que interactúa con la estancia consta de tres módulos sensores y actuadores inalámbricos, los cuales se describen a continuación (véase la Figura~\ref{fig:usr_nodos}):

\begin{figure}[H]
    \centering
    \begin{subfigure}[b]{0.32\textwidth}
        \centering
        \includegraphics[width=\textwidth]{Img/nodo_ambiente.jpg}
        \caption{Módulo de Ambiente ($N_1$)}
        \label{fig:usr_nodo_amb}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.32\textwidth}
        \centering
        \includegraphics[width=\textwidth]{Img/nodo_escritorio.jpg}
        \caption{Módulo de Escritorio ($N_2$)}
        \label{fig:usr_nodo_esc}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.32\textwidth}
        \centering
        \includegraphics[width=\textwidth]{Img/nodo_puerta.jpg}
        \caption{Módulo de Puerta ($N_3$)}
        \label{fig:usr_nodo_puerta}
    \end{subfigure}
    \caption{Componentes de hardware y nodos sensores instalados en la habitación.}
    \label{fig:usr_nodos}
\end{figure}

\begin{enumerate}
    \item \textbf{Módulo de Ambiente ($N_1$):} Mide la temperatura, la humedad y el nivel de ruido. Debe ubicarse en una zona de la pared libre de corrientes directas. Incluye el relé que controla el enchufe general.
    \item \textbf{Módulo de Escritorio ($N_2$):} Integra el sensor de presencia por radar y el láser. Debe colocarse sobre la mesa de trabajo, a 0.5-1.5 metros del usuario.
    \item \textbf{Módulo de Puerta ($N_3$):} Contiene el sensor magnético Reed. Se instala sobre el marco y la hoja de la puerta.
\end{enumerate}

\subsection{Conexión y Cableado de Periféricos}
Al ensamblar físicamente los nodos ESP32, asegúrese de que todos los sensores compartan una masa común (GND) y de no superar los $3.3\,\text{V}$ en las entradas lógicas (GPIO).

\subsubsection{Módulo de Ambiente (Nodo 1)}
\begin{itemize}
    \item \textbf{DHT11}: a 3.3V y datos al \textbf{GPIO 4}.
    \item \textbf{Fotorresistor LDR}: Divisor de tensión a 3.3V y salida analógica al \textbf{GPIO 32}.
    \item \textbf{KY-037 (Big Sound)}: Alimentado a 5V (VIN), salida digital al \textbf{GPIO 27}.
    \item \textbf{Módulo Relé}: Alimentado a 5V (VIN), control al \textbf{GPIO 26}.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.65\textwidth]{Img/conexion_nodo_ambiente.png}
    \caption{Diagrama de conexionado de periféricos en el Módulo de Ambiente.}
    \label{fig:conexion_ambiente}
\end{figure}

\subsubsection{Módulo de Escritorio (Nodo 2)}
\begin{itemize}
    \item \textbf{Radar mmWave HLK-LD2410C}: Alimentado a 5V (VIN). TX radar a \textbf{RX2 (GPIO 16)}, RX radar a \textbf{TX2 (GPIO 17)}.
    \item \textbf{Láser KY-008}: Pin de control lógico directo al \textbf{GPIO 12}.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.65\textwidth]{Img/conexion_nodo_escritorio.png}
    \caption{Diagrama de conexionado de periféricos para el Módulo de Escritorio.}
    \label{fig:conexion_escritorio}
\end{figure}

\subsubsection{Módulo de Puerta (Nodo 3)}
\begin{itemize}
    \item \textbf{Sensor Magnético (Reed Switch)}: Se conecta directamente entre el \textbf{GPIO 4} y GND aprovechando la resistencia interna \textit{pull-up}.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.65\textwidth]{Img/conexion_nodo_puerta.png}
    \caption{Diagrama de conexionado de periféricos para el Módulo de Puerta.}
    \label{fig:conexion_puerta}
\end{figure}

\subsection{Integración Inicial de Nodos (Programación ESPHome)}
Para que los nodos se conecten a la Raspberry Pi, deben ser programados por primera vez:
\begin{enumerate}
    \item Accede a la interfaz de ESPHome introduciendo la IP de la Raspberry en el puerto 6052 (ej. \texttt{http://100.x.x.x:6052}).
    \item Selecciona \textbf{"+ Add Device"} e introduce el nombre del nodo.
    \item Configura las credenciales de tu red Wi-Fi local dentro del código YAML.
    \item \textbf{Conexión Física Inicial}: Conecta el ESP32 al puerto USB de tu ordenador.
    \item Haz clic en \textbf{"Install"} y selecciona la opción para flashear mediante conexión por cable serial. Tras unos minutos, el firmware se cargará en la placa. 
    \item Una vez completado, el nodo puede instalarse en su ubicación definitiva y recibir actualizaciones inalámbricas (OTA) en el futuro.
\end{enumerate}

\subsection{Manual de la Plataforma de Monitorización}
El usuario final interactúa con la habitación mediante el cuadro de mandos Lovelace en Home Assistant.

\subsubsection{Acceso al Sistema}
\begin{itemize}
    \item \textbf{Desde Casa (Local)}: Conéctate al Wi-Fi doméstico. Abre el navegador web o la App de Home Assistant e ingresa la dirección local de la Raspberry Pi en el puerto 8123 (ej. \texttt{http://192.168.1.X:8123}).
    \item \textbf{Desde Fuera (Remoto)}: Activa la aplicación Tailscale en tu teléfono móvil. Luego abre la App de Home Assistant o el navegador e ingresa la dirección Tailscale asignada a la Raspberry Pi (ej. \texttt{http://100.x.x.x:8123}).
\end{itemize}

\subsubsection{Navegación por el Panel Lovelace}
Al iniciar sesión, se visualizan todos los dispositivos de la estancia:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{Img/ha_dashboard_lovelace1.png}
    \caption{Pantalla principal del panel de control Lovelace en Home Assistant.}
    \label{fig:usr_dashboard1}
\end{figure}

\begin{itemize}
    \item \textbf{Controles de Acciones}: Activa o desactiva la alarma, el modo noche, o el enchufe inteligente directamente con un toque en la tarjeta correspondiente.
    \item \textbf{Monitorización del Entorno}: Visualiza los valores instantáneos de temperatura, humedad y el nivel de ruido captado (alto o normal).
    \item \textbf{Presencia Inteligente}: Observa si la estancia se encuentra ocupada (basado en el radar de mmWave) y el estado físico de los accesos (barrera láser y contacto magnético de puerta).
\end{itemize}

Las gráficas del histórico permiten consultar la evolución térmica y la actividad de movimiento a lo largo del tiempo.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{Img/ha_dashboard_lovelace2.png}
    \caption{Sección de históricos y registros en Lovelace.}
    \label{fig:usr_dashboard2}
\end{figure}

\subsection{Manual de Comportamientos Inteligentes (Automatizaciones)}
El sistema opera en segundo plano tomando decisiones que facilitan el día a día sin requerir interacción manual constante:
\begin{itemize}
    \item \textbf{Luz Automática de Trabajo}: Se enciende sola cuando te sientas en el escritorio, apoyada por la detección milimétrica del radar LD2410, siempre y cuando la luminosidad de la sala (medida por el LDR) sea baja.
    \item \textbf{Alertas Ergonómicas (Pomodoro)}: Si permaneces 25 minutos continuos trabajando y sentado, la lámpara realizará un aviso visual (parpadeo) invitándote a realizar un descanso saludable.
    \item \textbf{Alarma Perimetral e Intrusión}: Estando activa, una interrupción del láser del escritorio o la apertura forzada de la puerta (detectada por el sensor Reed) desencadenará una alerta inmediata en tu teléfono móvil.
    \item \textbf{Ahorro Energético Ausente}: El sistema apagará automáticamente el relé de las luces tras 10 minutos de inactividad global absoluta en la habitación.
\end{itemize}

\subsection{Guía de Resolución de Incidencias}
A continuación, se ofrecen las soluciones a los problemas más frecuentes:

\begin{itemize}
    \item \textbf{P: Las placas ESP32 no conectan a la red Wi-Fi.}
    \begin{itemize}
        \item \textbf{R:} Comprueba que tu router transmita en la banda de $2.4\,\text{GHz}$. Los chips ESP32 no son compatibles con la frecuencia de $5\,\text{GHz}$.
    \end{itemize}
    \item \textbf{P: La luz automática no enciende al sentarme en la mesa.}
    \begin{itemize}
        \item \textbf{R:} Verifica el nivel que marca el sensor LDR en Home Assistant. Si el nivel de luz natural en la habitación es alto, la automatización ignorará el encendido de la lámpara.
    \end{itemize}
    \item \textbf{P: No se actualizan los datos de los sensores en el móvil cuando salgo de casa.}
    \begin{itemize}
        \item \textbf{R:} Asegúrate de tener habilitada y encendida la conexión VPN en la aplicación móvil de Tailscale y de contar con cobertura de datos 4G/5G.
    \end{itemize}
    \item \textbf{P: Un nodo aparece "No disponible" en el panel.}
    \begin{itemize}
        \item \textbf{R:} Desconecta y vuelve a conectar físicamente la alimentación (5V) del nodo. Si el problema persiste, verifica desde el panel de ESPHome en el servidor si coinciden las contraseñas de encriptación de la API.
    \end{itemize}
\end{itemize}
"""

with open(r"c:\Users\jacob\Downloads\TFG\Documento final\A_manual_usuario.tex", "w", encoding="utf-8") as f:
    f.write(tex_content)
    
print("A_manual_usuario.tex has been updated.")
