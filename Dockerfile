FROM python:3.12-alpine

# Directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema para que MySQL funcione en Alpine
RUN apk add --no-cache mariadb-connector-c-dev build-base

# Copiamos e instalamos librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para arrancar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]