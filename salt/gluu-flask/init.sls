flask_depends:
  pkg:
    - installed
    - pkgs:
      - git
      - libssl-dev
      - python
      - python-dev
      - software-properties-common
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

salt:
  pkgrepo:
    - managed
    - ppa: saltstack/salt
    - require:
      - pkg: flask_depends
    - require_in:
      - pkg: salt
  pkg:
    - installed
    - name: salt-master

python-pip:
  pkg:
    - purged

python-setuptools:
  pkg:
    - installed

{{ opts['cachedir'] }}/pip:
  file:
    - directory
    - user: root
    - group: root
    - mode: 550

{%- set version='6.0.8' %}

pip:
  file:
    - directory
    - name: /usr/local/lib/python{{ grains['pythonversion'][0] }}.{{ grains['pythonversion'][1] }}/dist-packages
    - makedirs: True
  archive:
    - extracted
    - name: {{ opts['cachedir'] }}/pip
    - source: https://pypi.python.org/packages/source/p/pip/pip-{{ version }}.tar.gz
    - source_hash: md5=2332e6f97e75ded3bddde0ced01dbda3
    - archive_format: tar
    - tar_options: z
    - if_missing: {{ opts['cachedir'] }}/pip/pip-{{ version }}
    - require:
      - file: {{ opts['cachedir'] }}/pip
  module:
{%- if not salt['file.file_exists']('/usr/local/bin/pip') -%}
    {#- force module to run if pip isn't installed yet #}
    - run
{%- else %}
    - wait
    - watch:
      - archive: pip
{%- endif %}
    - name: cmd.run
    - cmd: /usr/bin/python setup.py install
    - cwd: {{ opts['cachedir'] }}/pip/pip-{{ version }}
    - require:
      - pkg: python-pip
      - pkg: flask_depends
      - pkg: python-setuptools
      - file: pip
{%- if not salt['file.file_exists']('/usr/local/bin/pip') %}
      - archive: pip
{%- endif %}

virtualenv:
  file:
    - managed
    - name: {{ opts['cachedir'] }}/pip/virtualenv
    - contents: |
        virtualenv==1.9.1
    - user: root
    - group: root
    - mode: 440
    - require:
      - module: pip
  module:
{%- if not salt['file.file_exists']('/usr/local/bin/virtualenv') -%}
    {#- force module to run if virtualenv isn't installed yet #}
    - run
{%- else %}
    - wait
    - watch:
      - file: virtualenv
{%- endif %}
    - name: pip.install
    - requirements: {{ opts['cachedir'] }}/pip/virtualenv
    - require:
      - pkg: flask_depends
{%- if not salt['file.file_exists']('/usr/local/bin/virtualenv') %}
      - file: virtualenv
{%- endif %}

gluu-flask-requirements:
  file:
    - managed
    - name: {{ opts['cachedir'] }}/gluu-requirements.txt
    - source: https://raw.githubusercontent.com/GluuFederation/gluu-flask/42d6b16144d58aa5a7cca7813af4ba022d980986/requirements.txt
    - source_hash: md5=033c90fb4899df2024e26547661a5d90
    - user: root
    - group: root
    - mode: 440

gluu-flask:
  git:
    - latest
    - name: https://github.com/GluuFederation/gluu-flask.git
    - target: /usr/local/gluu-flask
    - require:
      - pkg: flask_depends
  virtualenv:
    - manage
    - name: /usr/local/gluu-flask/env
    - require:
      - git: gluu-flask
      - module: virtualenv
  module:
    - wait
    - name: pip.install
    - upgrade: True
    - bin_env: /usr/local/gluu-flask/env
    - requirements: {{ opts['cachedir'] }}/gluu-requirements.txt
    - require:
      - module: pip
    - watch:
      - file: gluu-flask-requirements
  file:
    - managed
    - name: /etc/init/gluu-flask.conf
    - source: salt://gluu-flask/upstart.jinja2
    - template: jinja
    - user: root
    - group: root
    - mode: 400
    - require:
      - module: gluu-flask
  service:
    - running
    - watch:
      - file: gluu-flask
  cmd:
    - wait
    - cwd: /usr/local/gluu-flask
    - name: env/bin/py.test tests --cov api --cov-report term-missing
    - watch:
      - service: gluu-flask
