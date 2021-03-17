FROM  python:3.7-alpine

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /
RUN  pip install -r /requirements.txt

RUN mkddir /app
COPY ./app /