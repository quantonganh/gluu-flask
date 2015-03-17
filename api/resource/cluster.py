# -*- coding: utf-8 -*-
'''/cluster resource'''
import uuid

from flask import url_for
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from api.model import GluuCluster
from api.database import db
from api.reqparser import cluster_reqparser


class Cluster(Resource):
    @swagger.operation(
        notes='Gives cluster info/state',
        nickname='getcluster',
        parameters=[],
        responseMessages=[
            {
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
    def get(self, cluster_id):
        obj = db.get(cluster_id, "clusters")
        if not obj:
            return {"code": 404, "message": "Cluster not found"}, 404
        return obj.as_dict()

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
    def delete(self, cluster_id):
        cluster = db.get(cluster_id, "clusters")
        if not cluster:
            return {"code": 404, "message": "Cluster not found"}, 404

        db.delete(cluster_id, "clusters")
        return {}, 204

    @swagger.operation(
        notes='update a cluster',
        nickname='editcluster',
        parameters=[
            {
                "name": "name",
                "description": "Name of the cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "description",
                "description": "Description of the purpose of the cluster.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "orgName",
                "description": "Full name of the Organization",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "orgShortName",
                "description": "Short word or abbreviation for the organization",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "city",
                "description": "City for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "state",
                "description": "State or province for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "countryCode",
                "description": "ISO 3166-1 two-character country code for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "admin_email",
                "description": "Admin email for the self-signed certifcates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "hostname_ldap_cluster",
                "description": "Hostname to use for the LDAP cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "hostname_oxauth_cluster",
                "description": "Hostname to use for the oxAuth authentication APIs",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "hostname_oxtrust_cluster",
                "description": "Hostname to use for the oxTrust admin interface website.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
        ],
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
        cluster = db.get(cluster_id, "clusters")
        if not cluster:
            return {"code": 404, "message": "Cluster not found"}, 404

        params = cluster_reqparser.parse_args()

        cluster.set_fields(params)
        db.update(cluster_id, cluster, "clusters")
        return cluster.as_dict()


class ClusterList(Resource):
    @swagger.operation(
        notes='Gives cluster info/state',
        nickname='listcluster',
        # responseClass=GluuCluster,
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "Cluster list information",
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            },
        ],
        summary='TODO'
    )
    def get(self):
        obj_list = db.all("clusters")
        return [item.as_dict() for item in obj_list]

    @swagger.operation(
        notes='Creates a new cluster',
        nickname='postcluster',
        parameters=[
            {
                "name": "name",
                "description": "Name of the cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "description",
                "description": "Description of the purpose of the cluster.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "orgName",
                "description": "Full name of the Organization",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "orgShortName",
                "description": "Short word or abbreviation for the organization",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "city",
                "description": "City for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "state",
                "description": "State or province for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "countryCode",
                "description": "ISO 3166-1 two-character country code for self-signed certificates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "admin_email",
                "description": "Admin email for the self-signed certifcates.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "hostname_ldap_cluster",
                "description": "Hostname to use for the LDAP cluster",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "hostname_oxauth_cluster",
                "description": "Hostname to use for the oxAuth authentication APIs",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "hostname_oxtrust_cluster",
                "description": "Hostname to use for the oxTrust admin interface website.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
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
        summary='Create a new cluster'
    )
    def post(self):
        params = cluster_reqparser.parse_args()

        cluster = GluuCluster()
        cluster.id = "{}".format(uuid.uuid4())
        cluster.set_fields(params)
        db.persist(cluster, "clusters")

        headers = {
            "Location": url_for("cluster", cluster_id=cluster.id),
        }
        return cluster.as_dict(), 201, headers
