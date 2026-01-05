# Usamos una imagen base liviana de Python
FROM python:3.12-slim

# Instalamos Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Configuramos el directorio de trabajo
WORKDIR /app

# Copiamos solo los archivos de configuración de poetry primero (para cachear capas)
COPY pyproject.toml poetry.lock ./

# Instalamos dependencias (sin crear entorno virtual dentro del contenedor, usamos el global)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiamos el código fuente
COPY src/ ./src/

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "src.guardian_silo.main:app", "--host", "0.0.0.0", "--port", "8000"]