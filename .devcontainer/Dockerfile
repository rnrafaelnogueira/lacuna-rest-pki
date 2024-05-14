FROM python:3.7.11-buster

RUN apt-get update && apt-get upgrade --yes && apt-get install python3-setuptools -y

RUN pip3 install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Define a pasta de trabalho
WORKDIR /app

# Copia o código fonte para a pasta de trabalho (se necessário)
COPY . .