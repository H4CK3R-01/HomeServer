FROM python:3.7-alpine

MAINTAINER Florian Kaiser <resiaknairolf@gmail.com>

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:9000", "app:app"]
