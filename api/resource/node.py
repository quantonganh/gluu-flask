# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Gluu
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
from flask import abort
from flask import current_app
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from api.database import db
from api.helper.model_helper import LdapModelHelper
from api.helper.model_helper import OxAuthModelHelper
from api.helper.model_helper import OxTrustModelHelper
from api.helper.model_helper import stop_ldap
from api.helper.docker_helper import DockerHelper
from api.helper.salt_helper import unregister_minion
from api.reqparser import node_reqparser


class Node(Resource):
    @swagger.operation(
        notes='Gives a node info/state',
        nickname='getnode',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "Node information",
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
    def get(self, node_id):
        obj = db.get(node_id, "nodes")
        if not obj:
            return {"code": 404, "message": "Node not found"}, 404
        return obj.as_dict()

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
                "code": 404,
                "message": "Node not found",
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

        if not node:
            return {"code": 404, "message": "Node not found"}, 404

        if node.type == "ldap":
            stop_ldap(node)

        # remove container
        docker = DockerHelper()
        docker.remove_container(node.id)

        # unregister minion
        unregister_minion(node.id)

        # remove node
        db.delete(node_id, "nodes")

        # removes reference from cluster, if any
        cluster = db.get(node.cluster_id, "clusters")
        if cluster:
            cluster.remove_node(node)
            db.update(cluster.id, cluster, "clusters")
        return {}, 204


class NodeList(Resource):
    @swagger.operation(
        notes='Gives node list info/state',
        nickname='listnode',
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "List node information",
            },
            {
                "code": 500,
                "message": "Internal Server Error"
            },
        ],
        summary='TODO'
    )
    def get(self):
        obj_list = db.all("nodes")
        return [item.as_dict() for item in obj_list]

    @swagger.operation(
        notes="""This API will create a new Gluu Server cluster node. This may take a while, so the process
is handled asyncronously by the Twisted reactor. It includes creating a new docker instance, deploying
the necessary software components, and updating the configuration of the target node and any
other dependent cluster nodes. Subsequent GET requests will be necessary to find out when the
status of the cluster node is available.""",
        nickname='postnode',
        parameters=[
            {
                "name": "cluster",
                "description": "The ID of the cluster--must exist",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            },
            {
                "name": "node_type",
                "description": "ldap | oxauth | oxtrust",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "form"
            }
        ],
        responseMessages=[
            {
                "code": 202,
                "message": "Accepted",
            },
            {
                "code": 400,
                "message": "Bad Request",
            },
            {
                "code": 500,
                "message": "Internal Server Error",
            }
        ],
        summary='TODO'
    )
    def post(self):
        params = node_reqparser.parse_args()
        salt_master_ipaddr = current_app.config["SALT_MASTER_IPADDR"]
        docker_base_url = current_app.config["DOCKER_SOCKET"]

        # check node type
        if params.node_type not in ("ldap", "oxauth", "oxtrust"):
            abort(400)

        # check that cluster id is valid else return with message and code
        cluster = db.get(params.cluster, "clusters")
        if not cluster:
            abort(400)

        if params.node_type == "ldap":
            helper_class = LdapModelHelper
        elif params.node_type == "oxauth":
            helper_class = OxAuthModelHelper
        elif params.node_type == "oxtrust":
            helper_class = OxTrustModelHelper

        helper = helper_class(cluster, salt_master_ipaddr, docker_base_url)
        print "build logpath: %s" % helper.logpath
        helper.setup()

        # Returns the HTTP response as ACCEPTED
        # TODO: what's the best way to monitor the result?
        return {}, 202
