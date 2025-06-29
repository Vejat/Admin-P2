FROM python:3.12-slim

WORKDIR /app

# Copiamos los requirements para aprovechar cache
COPY requirements.txt .

# Instalamos dependencias y email-validator
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install email-validator

# Creamos el directorio para la base de datos SQLite
RUN mkdir -p /app/data

# Copiamos el resto del cÃ³digo fuente
COPY ./app ./app

EXPOSE 8000

# Comando para ejecutar el servicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]