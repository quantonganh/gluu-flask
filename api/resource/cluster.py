# -*- coding: utf-8 -*-
'''/cluster resource'''
import uuid

from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from api.model import GluuCluster
from api.database import db
from api.reqparser import cluster_reqparser


class Cluster(Resource):
    """
    creats a empty gluu cluster
    cluster object holdes all states
    """
    @swagger.operation(
        notes='Gives cluster info/state',
        nickname='getcluster',
        parameters=[],
        responseMessages=[ {
              "code": 200,
              "message": "List cluster information",
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
        if cluster_id:
            obj = db.get(cluster_id, "clusters")
            if not obj:
                return {"code": 404, "message": "Cluster not found"}, 404
            return obj.as_dict()

        obj_list = db.all("clusters")
        return [item.as_dict() for item in obj_list]

    @swagger.operation(
        notes='Create a new cluster',
        nickname='postcluster',
        parameters=[
            {
                "name": "name",
                "description": "Name of the cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "description",
                "description": "Description of the purpose of the cluster.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "orgName",
                "description": "Full name of the Organization",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "orgShortName",
                "description": "Short word or abbreviation for the organization",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "city",
                "description": "City for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "state",
                "description": "State or province for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "countryCode",
                "description": "ISO 3166-1 two-character country code for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "admin_email",
                "description": "Admin email for the self-signed certifcates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "hostname_ldap_cluster",
                "description": "Hostname to use for the LDAP cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "hostname_oxauth_cluster",
                "description": "Hostname to use for the oxAuth authentication APIs",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "hostname_oxtrust_cluster",
                "description": "Hostname to use for the oxTrust admin interface website.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "ldaps_port",
                "description": "Hostname to use for the ldaps service for respective hostname_ldap_cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            }
        ],
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
        params = cluster_reqparser.parse_args()

        cluster = GluuCluster()
        cluster.id = "{}".format(uuid.uuid4())
        cluster.set_fields(params)
        db.persist(cluster, "clusters")
        return cluster.as_dict(), 201

    @swagger.operation(
        notes='delete a cluster',
        nickname='delcluster',
        parameters=[],
        responseMessages=[
            {
                "code": 204,
                "message": "Cluster deleted"
            },
            {
                "code": 500,
                "message": "Internal Server Error",
            },
        ],
        summary='TODO'
    )
    def delete(self, cluster_id):
        db.delete(cluster_id, "clusters")
        return {}, 204

    @swagger.operation(
        notes='update a cluster',
        nickname='editcluster',
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "Cluster updated"
            },
            {
                "code": 404,
                "message": "Cluster not found",
            },
            {
                "code": 500,
                "message": "Internal Server Error",
            },
        ],
        summary='TODO'
    )
    def put(self, cluster_id):
        params = cluster_reqparser.parse_args()

        cluster = db.get(cluster_id, "clusters")
        if not cluster:
            return {"code": 404, "message": "Cluster not found"}, 404

        cluster.set_fields(params)
        db.update(cluster_id, cluster, "clusters")
        return cluster.as_dict()
