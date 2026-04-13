# Imagen base estable para Python 3.7
FROM python:3.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Repositorios Archive y dependencias del sistema (Incluyendo Tkinter para Turtle)
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    libffi-dev \
    unixodbc-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    python3-tk \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requerimientos
COPY requirements.txt /app/

# Limpieza de requirements y configuración de PIP
RUN sed -i '/pkg_resources==0.0.0/d' requirements.txt && \
    pip install --no-cache-dir --upgrade "pip<23.1" "setuptools<68" "wheel" && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Comando de arranque
CMD ["gunicorn", "--bind", "0.0.0.0:50000", "gcs_coop.wsgi:application"]
