# -*- coding: utf-8 -*-
'''/node resource'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

class Node(Resource):
    """
    Node is a docker container runs salt-minions and points to salt-master
    Create gluu node
    """
    @swagger.operation(
        notes='Gives all nodes info/state',
        nickname='getnode',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "list node information"
            }
          ],
        summary = 'TODO'
        )
    def get(self, node_id):
        if node_id:
            return {'echo': 'list info/state of node no: {}'.format(node_id)}
        else:
            return {'echo': 'list of all nodes info/state'}

    @swagger.operation(
        notes='create a node',
        nickname='postnode',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "node created"
            }
          ],
        summary = 'TODO'
        )
    def post(self, node_id):
        return {'echo': 'node created'}

    @swagger.operation(
        notes='delete a node',
        nickname='delnode',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "node deleted"
            }
          ],
        summary = 'TODO'
        )
    def delete(self, node_id):
        return {'echo': 'node deleted'}
