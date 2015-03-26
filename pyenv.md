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
