# Gluu Server Flask Management API Server

## Overview

This is an API server to enable management of Gluu clusters.

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
