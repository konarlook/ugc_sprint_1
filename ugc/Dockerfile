FROM python:3.10

# Установка PostgreSQL клиента
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh
COPY src/. .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

EXPOSE 5000

ENTRYPOINT ["sh", "entrypoint.sh"]
