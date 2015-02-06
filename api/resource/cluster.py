# -*- coding: utf-8 -*-
'''/cluster resource'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

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
        notes='create a new cluster',
        nickname='postcluster',
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "cluster created"
            }
          ],
        summary = 'TODO'
        )
    def post(self, cluster_id):
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
