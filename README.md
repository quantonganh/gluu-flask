# Gluu Server Flask Management API Server

## Overview

This is an API server to enable management of Gluu clusters.

## Prerequisites

### Install docker.io

```
http://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit
```
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
$ nosetests tests.singleton
$ nosetests tests.cluster
```
