#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

from api.app import create_app
from api.settings import DevConfig, ProdConfig
from flask.ext import restful

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))

restapi = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return {'echo': 'hello world'}

restapi.add_resource(HelloWorld, '/bootstrap')

if __name__ == '__main__':
    app.run()