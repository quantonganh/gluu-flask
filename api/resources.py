# -*- coding: utf-8 -*-
'''api resources'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

class Bootstrap(Resource):
    """
    bootstrap gluu salt-master node
    docker minions will point to salt-master
    """
    @swagger.operation(
        notes='a test note',
        nickname='bootstrap',
        responseMessages=[
            {
              "code": 200,
              "message": "list node information"
            }
          ]
        )
    def get(self):
        return {'echo': 'list docker image ids and container ids'}

    @swagger.operation(
        notes='a test note',
        nickname='bootstrap',
        responseMessages=[
            {
              "code": 200,
              "message": "node created"
            }
          ]
        )
    def post(self):
        return {'echo': 'list newly created docker image ids and container ids'}

    @swagger.operation(
        notes='a test note',
        nickname='bootstrap',
        responseMessages=[
            {
              "code": 200,
              "message": "node deleted"
            }
          ]
        )
    def delete(self):
        return {'echo': 'list deleted docker image ids and container ids'}
