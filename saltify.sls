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
    - name: deb-src http://mirror-fpt-telecom.fpt.net/ubuntu/ {{ grains['oscodename'] }} main restricted universe multiverse
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

salt:
  pkgrepo:
    - managed
    - name: deb http://ppa.launchpad.net/saltstack/salt/ubuntu {{ grains['oscodename'] }} main
    - file: /etc/apt/sources.list.d/saltstack-salt.list
    - clean_file: True
    - require_in:
      - pkg: salt
  cmd:
    - run
    - name: wget -q -O- "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x4759FA960E27C0A6" | sudo apt-key add -
    - require:
      - pkg: flask_depends
      - pkgrepo: salt
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
    - source: https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
    - source_hash: md5=d843f5d9670cbd55f5187a199b43d2f8
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
    - source: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
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

gluu-flask:
  git:
    - latest
    - name: https://github.com/GluuFederation/gluu-flask.git
    - target: /root/gluu-flask
    - require:
      - pkg: git
  virtualenv:
    - managed
    - name: /root/gluu-flask/env
    - requirements: /root/gluu-flask/requirements.txt
    - require:
      - git: gluu-flask
  cmd:
    - wait
    - cwd: /root/gluu-flask
    - name: SALT_MASTER_IPADDR=127.0.0.1 env/bin/python run.py
    - watch:
      - virtualenv: gluu-flask
  module:
    - run
    - name: cmd.run
    - cwd: /root/gluu-flask
    - cmd: env/bin/py.test --cov api --cov-report term-missing
    - require:
      - cmd: gluu-flask
