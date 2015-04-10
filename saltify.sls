flask_depends:
  pkg:
    - installed
    - pkgs:
      - libssl-dev
      - python-dev
      - swig
      - wget
  pkgrepo:
    - managed
    - name: deb-src http://archive.ubuntu.com/ubuntu {{ grains['oscodename'] }} main restricted universe multiverse
    - file: /etc/apt/sources.list.d/gluu-src.list
    - clean_file: True
    - require_in:
      - cmd: flask_depends
  cmd:
    - run
    - name: apt-get -y build-dep openssl

docker:
  cmd:
    - run
    - name: wget -qO- https://get.docker.com/ubuntu | sh
    - unless: docker version
    - require:
      - pkg: flask_depends

software-properties-common:
  pkg:
    - installed

salt:
  pkgrepo:
    - managed
    - ppa: saltstack/salt
    - require:
      - pkg: software-properties-common
    - require_in:
      - pkg: salt
  pkg:
    - installed
    - name: salt-master

python:
  pkg:
    - installed

setuptools:
  file:
    - managed
    - name: /usr/local/sbin/ez_setup.py
    - source: https://bitbucket.org/pypa/setuptools/raw/99ee7f2/ez_setup.py
    - source_hash: md5=7b634f9185651639f69b64f313265126
    - require:
      - pkg: python
  cmd:
    - wait
    - name: /usr/bin/python /usr/local/sbin/ez_setup.py
    - unless: which easy_install
    - watch:
      - file: setuptools

pip:
  file:
    - managed
    - name: /usr/local/sbin/get-pip.py
    - source: https://github.com/pypa/pip/raw/701a80f/contrib/get-pip.py
    - source_hash: md5=d151ff23e488d8f579d68a7a5777badc
    - require:
      - cmd: setuptools
  cmd:
    - wait
    - name: /usr/bin/python /usr/local/sbin/get-pip.py
    - unless: which pip
    - watch:
      - file: pip

virtualenv:
  pip:
    - installed
    - require:
      - cmd: pip

git:
  pkg:
    - installed

{%- set home = salt['user.info']('root')['home'] %}
gluu-flask:
  git:
    - latest
    - name: https://github.com/GluuFederation/gluu-flask.git
    - target: {{ home }}/gluu-flask
    - require:
      - pkg: git
  virtualenv:
    - managed
    - name: {{ home }}/gluu-flask/env
    - requirements: {{ home }}/gluu-flask/requirements.txt
    - require:
      - git: gluu-flask
  cmd:
    - wait
    - cwd: {{ home }}/gluu-flask
    - name: SALT_MASTER_IPADDR={{ grains['ip_interfaces']['eth0'][0] }} nohup env/bin/python run.py > nohup.log 2>&1 &
    - watch:
      - virtualenv: gluu-flask
  module:
    - run
    - name: cmd.run
    - cwd: {{ home }}/gluu-flask
    - cmd: env/bin/py.test --cov api --cov-report term-missing
    - require:
      - cmd: gluu-flask
