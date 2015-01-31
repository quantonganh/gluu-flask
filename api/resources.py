# -*- coding: utf-8 -*-
'''api resources'''
from flask.ext.restful import Resource

class HelloWorld(Resource):
    def get(self):
        return {'echo': 'hello world'}
