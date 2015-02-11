#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import subprocess
from flask import g
from api.model import cluster 

from api.app import create_app
from api.settings import DevConfig, ProdConfig

HERE = os.path.abspath(os.path.dirname(__file__))

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

@app.before_first_request
def _init():
    print '** set dynamic configaration here **'

@app.before_request
def connect():
    #g.db = connect_db()
    print 'create db/fp connection and store it in g'

@app.teardown_request
def teardown_request(exception):
    db = g.get('db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(port = app.config['PORT'])
    #app.run(port = app.config['PORT'], use_reloader = app.config['RELOADER'])
