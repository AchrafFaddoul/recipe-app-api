FROM  python:3.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/api

COPY ./requirements.txt /usr/src/app/api/
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

COPY . /usr/src/app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]