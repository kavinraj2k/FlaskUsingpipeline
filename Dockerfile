
FROM python:3.9
WORKDIR /app
RUN apt-get update \
    && apt-get install -y pkg-config libsystemd-dev libdbus-1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80
CMD [ "python", "app.py" ]
