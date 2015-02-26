# gluu-flask Cluster Management API Server

## Overview

The gluu-flask server is used to enable management of Gluu Server clusters.
There is an ever-evolving [wiki page](http://www.gluu.co/gluu_salt) which describes
the design of the gluu-flask component.

## Prerequisites

### Ubuntu packages

```
$ sudo apt-get install libssl-dev python-dev swig
$ sudo apt-get build-dep openssl
```

### Install docker.io

Follow these instructions to install the Docker managed package for Ubuntu Trusty 14.04
[http://docs.docker.com/installation/ubuntulinux](http://docs.docker.com/installation/ubuntulinux/#docker-maintained-package-installation)

### Install salt-master

```
echo deb http://ppa.launchpad.net/saltstack/salt/ubuntu `lsb_release -sc` main | sudo tee /etc/apt/sources.list.d/saltstack.list
wget -q -O- "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x4759FA960E27C0A6" | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y salt-master
```

## Deployment

### Install pip and virtualenv

```
# wget -q -O- https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python -
# wget -q -O- https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python -
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

To run the application, type the following command in the shell,
and make sure `SALT_MASTER_IPADDR` environment variable is set and
pointed to salt-master IP address.

    $ SALT_MASTER_IPADDR=xxx.xxx.xxx.xxx env/bin/python run.py


## Testing

`$ env/bin/python py.test --cov api --cov-report term-missing`

## Flask Swagger Docs

gluu-flask publishes swagger API documentation. You should be able view this interactive HTML page that lets you play with the API to some extent.

http://localhost:8080/api/spec.html
