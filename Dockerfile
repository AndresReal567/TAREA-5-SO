# Dockerfile
FROM python:3.9-slim

# Instala tkinter y dependencias (X11)
RUN apt-get update \
 && apt-get install -y python3-tk \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py /app

CMD ["python3", "main.py"]

