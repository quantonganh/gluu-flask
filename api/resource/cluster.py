# -*- coding: utf-8 -*-
'''/cluster resource'''
import uuid

from flask import current_app
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from ..model import GluuCluster


class Cluster(Resource):
    """
    creats a empty gluu cluster
    cluster object holdes all states
    """
    @swagger.operation(
        notes='Gives cluster info/state',
        nickname='getcluster',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "list node information"
            }
        ],
        summary='TODO'
        )
    def get(self, cluster_id=None):
        if cluster_id:
            cluster = GluuCluster()
            data = cluster.get(cluster_id, current_app.config["DB"])
            return data

        # TODO: get all clusters
        return {'echo': 'all cluster info/state'}

    @swagger.operation(
        notes='Create a new cluster',
        nickname='postcluster',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "cluster created"
            }
        ],
        summary='Create a new cluster and persist json to disk.'
        )
    def post(self):
        c = GluuCluster()
        c.id = "{}".format(uuid.uuid4())
        c.description = "Test Cluster"
        c.persist(current_app.config["DB"])
        return {'echo': 'new cluster created'}

    @swagger.operation(
        notes='delete a cluster',
        nickname='delcluster',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "cluster deleted"
            }
        ],
        summary='TODO'
        )
    def delete(self, cluster_id):
        return {'echo': 'cluster deleted'}
