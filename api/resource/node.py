# -*- coding: utf-8 -*-
'''/node resource'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from ..model import ldapNode
from flask import g
from flask.ext.restful import reqparse

class Node(Resource):
    """
    Node is a docker container runs salt-minions and points to salt-master
    Create gluu node
    """
    @swagger.operation(
        notes='Gives node or nodes info/state',
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
    def get(self, node_id = None):
        if node_id:
            return {'echo': 'list info/state of node no: {}'.format(node_id)}
        else:
            return {'echo': 'list of all nodes info/state {}'.format(g.get('cluster',None))}

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
    def post(self):
        #post data: {"cluster":"id/name","node":"ldap"}
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'cluster', type=str, location='form',
            required=True, help='Cluster name or id',
        )
        post_parser.add_argument(
            'node', type=str, location='form',
            required=True, help='node type',
        )
        args = post_parser.parse_args()
        # clone relivent dockerfile
        # build image
        # deploy container
        # accept container cert in host salt-master
        # create ldapNode() object
        # populate ldapNode object
        # add ldapNode object into cluster object
        # save cluster object in db
        return {'echo': '{} node created in Cluster: {}'.format(args.node, args.cluster)}

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
