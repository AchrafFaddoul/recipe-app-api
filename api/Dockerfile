FROM  python:3.7-alpine

WORKDIR /usr/src/app/api
COPY ./requirements.txt /usr/src/app/api/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]