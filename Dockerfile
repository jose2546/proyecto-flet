FROM python:3.11-slim

WORKDIR /app

# Desactiva por completo los módulos de escritorio para entornos en la nube
ENV FLET_SERVER_ONLY=true

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponemos el puerto estándar que exige la nube
EXPOSE 8080

# Comando oficial para arrancar Flet como una aplicación web en producción
CMD ["python", "main.py"]
