include:
  - docker

weave:
  cmd:
    - run
    - name: wget -O /usr/local/bin/weave https://github.com/weaveworks/weave/releases/download/latest_release/weave
    - require:
      - pkg: wget
  module:
    - wait
    - name: cmd.run
    - cmd: chmod +x /usr/local/bin/weave
    - watch:
      - cmd: weave
