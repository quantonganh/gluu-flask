# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014 Gluu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''/node resource'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from ..model.gluu_cluster import GluuCluster
from ..model.ldap_node import ldapNode
from ..model.oxauth_node import oxauthNode
from ..model.oxtrust_node import oxtrustNode
from ..setup import nodeSetup
from flask import g
from flask import abort
from flask.ext.restful import reqparse
from api.database import db


def get_node_object(node=''):
    node_map = {
        'ldap' : ldapNode,
        'oxauth' : oxauthNode,
        'oxtrust' : oxtrustNode,
    }
    if node in node_map:
        node_obj = node_map[node]()
    else:
        node_obj = None
    return node_obj


class Node(Resource):
    """
    APIs for cluster node CRUD.
    """
    def __init__(self):
        self.available_docker_images = ['ldap', 'oxauth', 'oxtrust']

    @swagger.operation(
        notes='Gives node or nodes info/state',
        nickname='getnode',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "List node information",
            },
            {
                "code": 404,
                "message": "Node not found",
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            },
        ],
        summary='TODO'
    )
    def get(self, node_id=None):
        if node_id:
            obj = db.get(node_id, "nodes")
            if not obj:
                return {"code": 404, "message": "Node not found"}, 404
            return obj.as_dict()

        obj_list = db.all("nodes")
        return [item.as_dict() for item in obj_list]

    @swagger.operation(
        notes='create a node',
        nickname='postnode',
        parameters=[
            {
                "name": "cluster",
                "description": "The ID of the cluster--must exist",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            },
            {
                "name": "node_type",
                "description": "The type of the node: either ldap | oxauth | oxtrust",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "node created"
            },
            {
                "code": 400,
                "message": "Bad Request"
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            }
        ],
        summary='TODO'
    )
    def post(self):

        # Sample post data: {"cluster":"21389213","node_type":"ldap"}
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'cluster', type=str, location='form',
            required=True, help='Cluster id to which this node will be added.',
        )
        post_parser.add_argument(
            'node_type', type=str, location='form',
            required=True, help='ldap | oxauth | oxtrust',
        )
        args = post_parser.parse_args()

        # check node type
        if args.node_type not in self.available_docker_images:
            abort(400)

        # check that cluster name or id is valid else return with message and code
        cluster = db.get(args.cluster, GluuCluster)
        if not cluster:
            abort(400)

        # MIKE: I think the business logic should be implemented in helper classes.
        # I'd like to see the code in this API be readable.

        if args.node_type == "ldap":
            # (1) Create the model for this new ldap node. For replication, you will need
            # to use the ip address of docker instance as hostname--not the cluster
            # ldap hostname. For the four ports (ldap, ldaps, admin, jmx), try to use the default
            # ports unless they are already in use, at which point it should chose a random
            # port over 10,000. Note these ports will need to be open between the ldap docker instances
            node = ldapNode(cluster_name = cluster.name)
            # (2) Start job to create docker instance
            run_container(node)
            # (3) Render opendj-setup.properties
            render_ldap_properties(node)
            # (4) Start job to run /opt/opendj/setup and dsconfig commands
            run_ldap_setup(node)
            # (5) Start job to import data. If no ldap nodes exist, import auto-generated
            # base ldif data; otherwise initialize data from existing ldap node. Also to
            # create fully meshed replication, update the other ldap nodes to use this new
            # ldap node as a master.
            #
            # from helpers import *
            #
            # newLdapNode = None
            #
            # try:
            #     newLdapNode = LdapModelHelper(args.cluster)
            # except:
            #     logs.error("could not create new ldap model for %s" % args.cluster
            #     abort(400)
            #
            # try:
            #     d = dockerHelper(newLdapNode)
            # except:
            #     logs.error("could not new docker instance for ldap node %s" % str(newLdapNode)
            #     abort(400)
            #
            # try:
            #     s = saltHelper(newLdapNode)
            # except:
            #     logs.error("Error configuring salt minion for %s" % str(newLdapNode)
            pass

        elif args.node_type == "oxauth":
            # (1) generate oxauth-ldap.properties, oxauth-config.xml
            # oxauth-static-conf.json; (2) Create or copy key material to /etc/certs;
            # (3) Configure apache httpd to proxy AJP:8009; (4) configure tomcat
            # to run oxauth war file.
            pass

        elif args.node_type == "oxtrust":
            # (1) generate oxtrustLdap.properties, oxTrust.properties,
            # oxauth-static-conf.json, oxTrustLogRotationConfiguration.xml,
            # (2) Create or copy key material to /etc/certs
            # (3) Configure apache httpd to proxy AJP:8009; (4) configure tomcat
            # to run oxtrust war file
            pass

        # get relevent dockerfile
        # build image
        image = get_image(args.node_type)
        # run setup using salt
        ns = nodeSetup(node)
        ns.setup()

        # add ldapNode object into cluster object
        db.persist(node)
        cluster.add_node(node)
        db.update(cluster)
        return {'status_code': 201, 'message': '{} node created in Cluster: {}'.format(args.node_type, args.cluster)}

    @swagger.operation(
        notes='delete a node',
        nickname='delnode',
        parameters=[],
        responseMessages=[
            {
              "code": 204,
              "message": "Node deleted",
            },
            {
                "code": 500,
                "message": "Internal Server Error",
            },
        ],
        summary='TODO'
    )
    def delete(self, node_id):
        node = db.get(node_id, "nodes")

        if node:
            # remove node
            db.delete(node_id, node)

            # removes reference from cluster
            cluster = db.get(node.cluster_id, GluuCluster)
            cluster.remove_node(node)
            db.update(cluster)
        return {}, 204
