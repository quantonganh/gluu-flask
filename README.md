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

### Install docker

Follow these instructions to install the package for Ubuntu Trusty 14.04 managed by docker.com:
[http://docs.docker.com/installation/ubuntulinux](http://docs.docker.com/installation/ubuntulinux/#docker-maintained-package-installation)

For the impatient, just type:

```
$ curl -sSL https://get.docker.com/ubuntu/ | sudo sh
```
After install, you should see

```
$ sudo docker version
Client version: 1.5.0
Client API version: 1.17
Go version (client): go1.4.1
Git commit (client): a8a31ef
OS/Arch (client): linux/amd64
Server version: 1.5.0
Server API version: 1.17
Go version (server): go1.4.1
Git commit (server): a8a31ef
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
$ wget -q -O- https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python -
$ wget -q -O- https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python -
$ export PATH="/usr/local/bin:$PATH"
$ pip install virtualenv
```
### Clone the project

```
$ git clone https://github.com/GluuFederation/gluu-flask.git
$ cd gluu-flask
$ virtualenv env
$ env/bin/pip install -r requirements.txt
```

#### Pyenv
You can use pyenv as an alternative for virtualenv

```
$ sudo apt-get install curl git-core gcc make zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libssl-dev
$ curl -L https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

Shell commands that should be added to ~/.bashrc or equivalent

```
export PYENV_ROOT="${HOME}/.pyenv"

if [ -d "${PYENV_ROOT}" ]; then
  export PATH="${PYENV_ROOT}/bin:${PATH}"
  eval "$(pyenv init -)"
fi
```

And then

```
$ . ~/.bashrc
$ pyenv install 2.7.6
$ pyenv global 2.7.6
$ pyenv virtualenv gluu-flask
$ cd gluu-flask/
$ pyenv local gluu-flask
$ pip install -r requirements.txt
```

## Run

To run the application, type the following command in the shell,
and make sure `SALT_MASTER_IPADDR` environment variable is set and
pointed to salt-master IP address.

```
$ SALT_MASTER_IPADDR=xxx.xxx.xxx.xxx env/bin/python run.py
```


## Testing

```
$ env/bin/py.test tests --cov api --cov-report term-missing
```

## Flask Swagger Docs

gluu-flask publishes swagger API documentation. You should be able view this interactive HTML page that lets you play with the API to some extent.

http://localhost:8080/api/spec.html
