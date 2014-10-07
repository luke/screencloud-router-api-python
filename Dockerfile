FROM ubuntu:14.04
MAINTAINER screencloud

# I can't live without this alias
RUN echo "alias 'll=ls -al'" >> /etc/bash.bashrc

# Get the system up to scratch
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# Install python stuffs
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libpq-dev

# Confd to manage configuration from environment vars or etcd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget
RUN wget -O /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v0.6.2/confd-0.6.2-linux-amd64
RUN chmod +x /usr/local/bin/confd
RUN mkdir -p /etc/confd/{conf.d,templates}

# Somewhere to put the application
RUN mkdir -p /srv/app
WORKDIR /srv/app

# Install the application's python requirements
COPY requirements.txt /srv/app/
RUN pip install -r requirements.txt

# Get the code into place
COPY . /srv/app

EXPOSE 5000
CMD ["./scripts/run.sh"]
