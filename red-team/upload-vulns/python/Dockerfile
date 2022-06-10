FROM python:3.10

WORKDIR /app
ADD ./app/requirements.txt /app
RUN apt-get update -y && \
    apt-get install -y netcat && \
    pip install -r requirements.txt

ADD ./app /app
