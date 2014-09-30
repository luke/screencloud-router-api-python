FROM ubuntu:14.04
MAINTAINER screencloud

RUN echo "alias 'll=ls -al'" >> /etc/bash.bashrc

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libpq-dev

RUN mkdir -p /srv/app
WORKDIR /srv/app

COPY requirements.txt /srv/app/
RUN pip install -r requirements.txt

COPY . /srv/app

EXPOSE 5000
CMD ["gunicorn", "--bind=:5000", "--workers=1", "run:wsgi_app", "--chdir=scripts", "--log-level=debug", "--log-file=/dev/stderr", "--access-logfile=/dev/stdout"]
