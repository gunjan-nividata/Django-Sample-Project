FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y gettext

# Requirements are installed here to ensure they will be cached.
ADD ./requirements /requirements

WORKDIR /app

RUN pip install -r /requirements/local.txt

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ADD . /app