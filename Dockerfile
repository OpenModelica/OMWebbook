# ---------------------------
# Base image
# ---------------------------
FROM ubuntu:24.04

LABEL maintainer="Arunkumar Palanisamy <arunkumar.palanisamy@liu.se>"

# ---------------------------
# Set locale for OpenModelica
# ---------------------------
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV HOME=/home/omuser
ENV MODELICAPATH=/home/omuser/.openmodelica/libraries
ENV PATH="/venv/bin:$PATH"

# ---------------------------
# Install all system packages needed
# ---------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gnupg wget curl ca-certificates lsb-release \
        software-properties-common \
        python3 python3-venv python3-pip python3-dev \
        build-essential git nginx supervisor &&\
    rm /etc/nginx/sites-enabled/default && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Add and install OpenModelica apt repository (latest method)
# ---------------------------
RUN wget -q https://build.openmodelica.org/apt/openmodelica.asc -O /usr/share/keyrings/openmodelica.asc && \
    echo "deb [signed-by=/usr/share/keyrings/openmodelica.asc] https://build.openmodelica.org/apt $(lsb_release -cs) release" \
    | tee /etc/apt/sources.list.d/openmodelica.list && \
    apt-get update && \
    # Install mininmal omc and omlibrary
    apt-get install -y --no-install-recommends omc omlibrary && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# Python environment
# ---------------------------
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade pip && \
    /venv/bin/pip install --no-cache-dir \
        git+https://github.com/OpenModelica/OMPython.git \
        flask \
        gunicorn \
        futures

# ---------------------------
# Create non-root user for OpenModelica & gunicorn
# ---------------------------
RUN useradd -ms /bin/bash omuser && \
    mkdir -p /home/omuser/.openmodelica/libraries && \
    chown -R omuser:omuser /home/omuser

# ---------------------------
# Nginx configuration
# ---------------------------
COPY flask.conf /etc/nginx/sites-available/flask.conf
RUN ln -s /etc/nginx/sites-available/flask.conf \
          /etc/nginx/sites-enabled/flask.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf

# ---------------------------
# Supervisor configuration
# ---------------------------
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ---------------------------
# Application code
# ---------------------------
WORKDIR /OMWebbook
COPY . /OMWebbook

# ---------------------------
# Expose port
# ---------------------------
#EXPOSE 80

# ---------------------------
# HEALTHCHECK
# ---------------------------
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
#   CMD curl -f http://localhost || exit 1

# ---------------------------
# Start supervisord
# ---------------------------
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
