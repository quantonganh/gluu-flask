wget:
  pkg:
    - installed

docker:
  cmd:
    - run
    - name: wget -qO- https://get.docker.com/ubuntu | sh
    - unless: docker version
    - require:
      - pkg: wget
