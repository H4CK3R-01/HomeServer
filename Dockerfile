FROM python:3.7-alpine

MAINTAINER Florian Kaiser <resiaknairolf@gmail.com>

RUN mkdir /app

COPY app/ /app

RUN pip3 install -r app/requirements.txt

CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:9000", "app:create_app()"]
