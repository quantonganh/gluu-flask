#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from crochet import setup as crochet_setup

from api.app import create_app
from api.settings import DevConfig, ProdConfig

HERE = os.path.abspath(os.path.dirname(__file__))

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

if __name__ == '__main__':
    crochet_setup()
    app.run(port=app.config['PORT'])
    #app.run(port = app.config['PORT'], use_reloader = app.config['RELOADER'])
