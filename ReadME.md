🚗 Carro Seguidor de Línea con PID — Proyecto Docker + Tkinter



Este proyecto implementa un carro virtual que sigue una pista curva utilizando Python y Tkinter como interfaz gráfica. Un controlador PID (Proporcional–Integral–Derivativo) permite al vehículo corregir su trayectoria automáticamente. La aplicación puede ejecutarse tanto de forma local como dentro de un contenedor Docker.
Desarrollado como parte de la Tarea 5 del curso de Sistemas Operativos.

📁 Estructura del Proyecto
bash
Copy
Edit
carro_tkinter/
├── main.py        # Código principal del simulador del carro
├── Dockerfile     # Configuración para entorno Docker
└── README.md      # Instrucciones y documentación
🧠 Descripción General
Interfaz gráfica creada con Tkinter.

Controlador PID implementado desde cero.

Pista con tres curvas circulares completas (loops).

El vehículo ajusta automáticamente su dirección para mantenerse sobre la línea negra.

Preparado para ejecutarse en sistemas Linux o en contenedores Docker.

🧪 Requisitos para Ejecución Local
Python 3.7 o superior

Tkinter (en Ubuntu se instala con):

bash
Copy
Edit
sudo apt update
sudo apt install -y python3-tk
▶️ Ejecución Local
bash
Copy
Edit
git clone https://github.com/tu_usuario/carro_tkinter.git
cd carro_tkinter
python3 main.py
🐳 Ejecución con Docker
1. Construir la imagen
bash
Copy
Edit
docker build -t carro_tkinter .
2. Conceder permisos a Docker para usar el servidor gráfico
bash
Copy
Edit
xhost +local:docker
3. Ejecutar el contenedor
bash
Copy
Edit
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  carro_tkinter


⚙️ Características Técnicas
Pista compuesta por tres arcos circulares de 360°, con un ancho de 60 px.
Sensor central frontal simula la detección de línea.
El carro inicia en el primer loop y sigue automáticamente la trayectoria negra.
Interfaz gráfica portable, compatible con Linux y Docker.


