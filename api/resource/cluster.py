# -*- coding: utf-8 -*-
'''/cluster resource'''
from flask.ext.restful import Resource, reqparse
from flask_restful_swagger import swagger
from ..model import cluster 

class Cluster(Resource):
    """
    creats a empty gluu cluster
    cluster object holdes all states
    """
    @swagger.operation(
        notes='Gives cluster info/state',
        nickname='getcluster',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "list node information"
            }
          ],
        summary = 'TODO'
        )
    def get(self, cluster_id = None):
        if cluster_id:
            return {'echo': 'list cluster info of cluster: {}'.format(cluster_id)}
        else:
            return {'echo': 'all cluster info/state'}

    @swagger.operation(
        notes='Create a new cluster',
        nickname='postcluster',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "cluster created"
            }
          ],
        summary = 'Create a new cluster and persist json to disk.'
        )
    def post(self):
        c = cluster()
        c.id = "12345"
        c.description = "Test Cluster"
        c.persist()
        return {'echo': 'new cluster created'}

    @swagger.operation(
        notes='delete a cluster',
        nickname='delcluster',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "cluster deleted"
            }
          ],
        summary = 'TODO'
        )
    def delete(self, cluster_id):
        return {'echo': 'cluster deleted'}
