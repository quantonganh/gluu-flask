# gluu-flask Cluster Management API Server

## Overview

The gluu-flask server is used to enable management of Gluu Server clusters.
There is an ever-evolving [wiki Page](http://www.gluu.co/gluu_salt) which describes
the design and goals of the components with which the gluu-flask api server interacts.

## Prerequisites

### Install docker.io

Follow these instructions to install the Docker managed package for Ubuntu Trusty 14.04 
[http://docs.docker.com/installation/ubuntulinux/#docker-maintained-package-installation](http://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit)

### Install salt-master

```
echo deb http://ppa.launchpad.net/saltstack/salt/ubuntu `lsb_release -sc` main | sudo tee /etc/apt/sources.list.d/saltstack.list
wget -q -O- "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x4759FA960E27C0A6" | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y salt-master
```

### Clone gluu-docker
Clone it into /tmp or any location you like.
```
git clone git@github.com:GluuFederation/gluu-docker.git
```

### Build images
Put your host ip in /tmp/gluu-docker/ubuntu/14.04/saltminion/minion file.
you must create saltminion image first.

```
sudo docker build -q --rm --force-rm -t saltminion /tmp/gluu-docker/ubuntu/14.04/saltminion
sudo docker build -q --rm --force-rm -t gluuopendj /tmp/gluu-docker/ubuntu/14.04/gluuopendj
sudo docker build -q --rm --force-rm -t gluuoxauth /tmp/gluu-docker/ubuntu/14.04/gluuoxauth
sudo docker build -q --rm --force-rm -t gluuoxtrust /tmp/gluu-docker/ubuntu/14.04/gluuoxtrust
sudo docker build -q --rm --force-rm -t gluuhttpd /tmp/gluu-docker/ubuntu/14.04/gluuhttpd
sudo docker build -q --rm --force-rm -t gluushib /tmp/gluu-docker/ubuntu/14.04/gluushib
sudo docker build -q --rm --force-rm -t gluucas /tmp/gluu-docker/ubuntu/14.04/gluucas
sudo docker build -q --rm --force-rm -t gluuasimba /tmp/gluu-docker/ubuntu/14.04/gluuasimba
```

## Deployment

### Install pip and virtualenv

```
# curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python -
# curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python -
# export PATH="/usr/local/bin:$PATH"
# pip install virtualenv

```
### Clone the project 

```
$ git clone https://github.com/GluuFederation/gluu-flask.git
$ cd gluu-flask
$ virtualenv env
$ env/bin/pip install -r requirements.txt

```

## Run
Just launch `run.py`

## Test
```
$ nosetests testapi
$ nosetests tests.singleton
$ nosetests tests.cluster
```
