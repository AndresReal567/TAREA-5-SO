# 🚗 Carro Seguidor de Línea con PID — Proyecto Docker + Tkinter

Este proyecto implementa un **carro virtual que sigue una pista curva** utilizando Python con **Tkinter** como interfaz gráfica y un controlador **PID** para corregir el rumbo. Está preparado para ejecutarse localmente o dentro de un contenedor **Docker**, y fue desarrollado como parte del proyecto de sistemas operativos (Tarea 5).

---

## 📂 Estructura del Proyecto

carro_tkinter/ ├── main.py # Código Python del carro seguidor ├── Dockerfile # Configuración del contenedor Docker └── README.md # Instrucciones de uso y documentación


---

## 🧠 Descripción General

- Interfaz gráfica generada con **Tkinter**.
- Algoritmo de control basado en **PID (Proporcional–Integral–Derivativo)**.
- Pista compuesta por **tres curvas circulares** (loops).
- El vehículo ajusta su dirección de forma automática para mantenerse sobre la línea negra.
- Totalmente portable mediante Docker.

---

## 🧪 Requisitos Locales

- Python 3.7 o superior
- Tkinter (en Ubuntu puedes instalarlo con):

```bash
sudo apt update
sudo apt install -y python3-tk
 
 Ejecución Local
 git clone https://github.com/tu_usuario/carro_tkinter.git
cd carro_tkinter
python3 main.py

Ejecución con Docker
docker build -t carro_tkinter .
xhost +local:docker

docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  carro_tkinter

Características Técnicas
Pista formada por tres arcos (360°) con un ancho de 60 px.

Sensor frontal central detecta superposición con la pista.

El carro inicia en el primer loop, se desplaza automáticamente y sigue la trayectoria negra.

Interfaz completamente portable con Docker y compatible con Linux.

Autor
Andrés Felipe Rojas Caro
Universidad / Curso: Sistemas Operativos
