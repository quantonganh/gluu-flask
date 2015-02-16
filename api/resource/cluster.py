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
              "message": "List node information",
            },
            {
                "code": 404,
                "message": "Cluster not found",
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            },
        ],
        summary='TODO'
        )
    def get(self, cluster_id=None):
        cluster = GluuCluster()

        if cluster_id:
            data = cluster.get(cluster_id, current_app.config["DB"])
            if not data:
                return {"code": 404, "message": "Cluster not found"}, 404
            return data

        data = cluster.all(current_app.config["DB"])
        return data

    @swagger.operation(
        notes='Create a new cluster',
        nickname='postcluster',
        parameters=[],
        responseMessages=[
            {
                "code": 201,
                "message": "Created",
            },
            {
                "code": 500,
                "message": "Internal Server Error",
            },
        ],
        summary='Create a new cluster and persist json to disk.'
        )
    def post(self):
        c = GluuCluster()
        c.id = "{}".format(uuid.uuid4())
        c.description = "Test Cluster"
        c.persist(current_app.config["DB"])
        return c.__dict__, 201

    @swagger.operation(
        notes='delete a cluster',
        nickname='delcluster',
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "Cluster deleted"
            },
            {
                "code": 404,
                "message": "Cluster not found"
            },
            {
                "code": 500,
                "message": "Internal Server Error",
            },
        ],
        summary='TODO'
        )
    def delete(self, cluster_id):
        cluster = GluuCluster()
        deleted = cluster.delete(cluster_id, current_app.config["DB"])
        if deleted:
            return {"code": 200, "message": "Cluster deleted"}
        return {"code": 404, "message": "Cluster not found"}, 404
