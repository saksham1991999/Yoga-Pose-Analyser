FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

RUN apt-get update

RUN apt-get -qq -y install binutils libproj-dev gdal-bin

WORKDIR /usr/src/app
COPY requirements.txt ./

ADD . /usr/src/app/
RUN pip install -r requirements.txt

#RUN python manage.py makemigrations
#RUN python manage.py migrate