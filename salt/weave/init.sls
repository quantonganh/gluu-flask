include:
  - docker

weave:
  cmd:
    - run
    - name: wget -O /usr/local/bin/weave https://github.com/weaveworks/weave/releases/download/latest_release/weave
    - require:
      - pkg: wget
  file:
    - managed
    - name: /usr/local/bin/weave
    - user: root
    - group: root
    - mode: 755
    - require:
      - cmd: weave
