gluu-server:
  service:
    - dead
  file:
    - absent
    - name: /etc/init/gluu-flask.conf

{%- for file in ('/usr/local/gluu-flask', '/usr/local/sbin/get-pip.py', '/usr/local/sbin/ez_setup.py') %}
{{ file }}:
  file:
    - absent
{%- endfor %}

salt-master:
  service:
    - dead
  pkg:
    - purged
    - require:
      - service: salt-master
  pkgrepo:
    - absent
    - ppa: saltstack/salt
    - require:
      - pkg: salt-master
