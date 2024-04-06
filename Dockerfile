FROM python:3.10.5-alpine3.16
RUN apt-get update && apt-get install -y git
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

