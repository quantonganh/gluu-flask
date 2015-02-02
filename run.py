#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

from api.app import create_app
from api.settings import DevConfig, ProdConfig
#from api.extensions import restapi
from flask.ext import restful
from flask_restful_swagger import swagger

#import resources
from api.resources import Bootstrap

HERE = os.path.abspath(os.path.dirname(__file__))

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

#restapi = restful.Api()
restapi = swagger.docs(restful.Api(app), apiVersion='0.1')
#restapi.init_app(app)
restapi.add_resource(Bootstrap, '/bootstrap')
#restapi.init_app(app)

if __name__ == '__main__':
    app.run(port = app.config['PORT'])