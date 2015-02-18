# -*- coding: utf-8 -*-
'''/node resource'''
import sys
import subprocess
import uuid
# from random import randrange
# from time import sleep

# from flask import g
# from flask import abort
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask_restful_swagger import swagger

from api.database import db
from api.model import GluuCluster
from api.model import ldapNode


def run(command, exit_on_error=True, cwd=None):
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT,
                                       shell=True, cwd=cwd)
    except subprocess.CalledProcessError, e:
        if exit_on_error:
            sys.exit(e.returncode)
        else:
            raise


def get_image(name='', docker_base_url='unix://var/run/docker.sock'):
    # an example response of get_image()
    """
    [{u'Created': 1422048669,
    u'Id': u'e348da14b96d85f1dfec380b53dfb106ea1fb4723f93fa8619ad798fd9509f7c',
    u'ParentId': u'26bc41e2ffeec6cff2d1880f378e308398662d5180adfda0689e37e081736200',  # noqa
    u'RepoTags': [u'gluuopendj:latest'],
    u'Size': 0,
    u'VirtualSize': 260371028}]
    or
    []
    """
    image = None

    try:
        from docker import Client
        c = Client(base_url=docker_base_url)
        image = c.images(name)
    except:
        # TODO add logging
        print "Error making connection to Docker Server"
    return image


def get_node_object(node=''):
    node_map = {
        'gluuopendj': ldapNode,
        # 'oxauth': oxauthNode,
        # 'oxtrust': oxtrustNode,
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
        self.available_docker_images = ['gluuopendj', 'oxauth', 'oxtrust']

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
                "description": "The type of the node: either ldap | oxauth | oxtrust",  # noqa
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
              "code": 201,
              "message": "Node created"
            },
            {
              "code": 400,
              "message": "Bad Request"
            },
            {
              "code": 422,
              "message": "Unprocessable Entity",
            },
            {
              "code": 500,
              "message": "Internal Server Error"
            }
          ],
        summary='TODO'
        )
    def post(self):
        # post data: {"cluster":"id/name","node_type":"gluuopendj"}
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'cluster', type=str, location='form',
            required=True, help='Cluster ID',
        )
        post_parser.add_argument(
            'node_type', type=str, location='form',
            required=True, help='gluuopendj | oxauth | oxtrust',
        )
        args = post_parser.parse_args()

        # check that cluster name or id is valid
        # else return with message and code
        cluster = db.get(args.cluster, GluuCluster)
        if not cluster:
            return {"status": 422, "message": "non-existant cluster"}, 422

        # # get relivent dockerfile
        # # build image
        # image = get_image(args.node_type)
        # if not image and args.node_type in self.available_docker_images:
        #     run('mkdir /tmp/{}'.format(args.node_type))
        #     raw_url = 'https://raw.githubusercontent.com/GluuFederation/gluu-docker/master/ubuntu/14.04/{}/Dockerfile'.format(args.node_type)  # noqa
        #     run('wget -q {} -P /tmp/{}'.format(raw_url, args.node_type))
        #     run('docker build -q --rm --force-rm -t {} {}'.format(args.node_type, '/tmp/{}'.format(args.node_type)))  # noqa
        #     run('rm -rf /tmp/{}'.format(args.node_type))
        # else:
        #     return abort(400)

        # # deploy container
        # con_name = '{0}_{1}_{2}'.format(args.node_type, args.cluster, randrange(101, 999))
        # cid = run('docker run -d -P --name={0} {1}'.format(con_name, args.node_type))
        # scid = cid.strip()[:-(len(cid)-12)]

        # # accept container cert in host salt-master
        # sleep(10)
        # run('salt-key -y -a {}'.format(scid))

        # create ldapNode() object
        node = get_node_object(args.node_type)

        # # populate ldapNode object
        # node.id = scid
        node.id = "{}".format(uuid.uuid4())
        # node.name = con_name
        node.type = args.node_type
        node.cluster_id = cluster.id

        # # run setup using salt
        # node.setup()

        # add node object into cluster object
        db.persist(node)
        cluster.add_node(node)
        db.update(cluster)
        return node.as_dict(), 201

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
