#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

from api.app import create_app
from api.settings import DevConfig, ProdConfig
from flask import jsonify

HERE = os.path.abspath(os.path.dirname(__file__))

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

def init_data_dir():
    if not os.path.isdir(app.config['DATA_DIR']):
        os.mkdir(app.config['DATA_DIR'])
    if not os.path.exists(app.config['CLUSTER_FILE']):
        with open(app.config['CLUSTER_FILE'], 'w') as fp:
            fp.write('{"name":"gluu"}')

def load_data():
    with open(app.config['CLUSTER_FILE'], 'r') as fp:
        app.config['gcluster'] = json.loads(fp.read())

def save_data():
    pass

if __name__ == '__main__':
    print "Starting gluu api server..."
    init_data_dir()
    load_data()
    app.run(port = app.config['PORT'], use_reloader=app.config['RELOADER'])
    save_data()
    print "Stoping gluu api server..."
