# -*- coding: utf-8 -*-
'''/node resource'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from ..model import ldapNode, GluuCluster
from flask import g
from flask import abort
from flask import current_app
from random import randrange
from flask.ext.restful import reqparse
import subprocess
import sys
from time import sleep

def run(command, exit_on_error=True, cwd=None):
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, cwd=cwd)
    except subprocess.CalledProcessError, e:
        if exit_on_error:
            sys.exit(e.returncode)
        else:
            raise

def get_image(name = '', docker_base_url='unix://var/run/docker.sock'):
    try:
        from docker import Client
        c = Client(base_url=docker_base_url)
        return c.images(name)
    except:
        # TODO add logging
        print "Error making connection to Docker Server"
    return None

def get_node_object(node = ''):
    node_map = {
        'gluuopendj' : ldapNode,
        #'oxauth' : oxauthNode,
        #'oxtrust' : oxtrustNode,
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
        parameters = [
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
        summary = 'TODO'
        )
    def post(self):
        #post data: {"cluster":"id/name","node_type":"gluuopendj"}
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'cluster', type=str, location='form',
            required=True, help='Cluster name or id',
        )
        post_parser.add_argument(
            'node_type', type=str, location='form',
            required=True, help='ldap | oxauth | oxtrust',
        )
        args = post_parser.parse_args()

        # check node type
        if not args.node_type in self.available_docker_images:
            abort(400)

        # check that cluster name or id is valid else return with message and code
        cluster = GluuCluster(args.cluster, current_app.config["DB"])
        if not cluster:
            abort(400)

        # get relivent dockerfile
        # build image
        image = get_image(args.node_type)
        # an example responce of get_image()
        """
            [{u'Created': 1422048669,
            u'Id': u'e348da14b96d85f1dfec380b53dfb106ea1fb4723f93fa8619ad798fd9509f7c',
            u'ParentId': u'26bc41e2ffeec6cff2d1880f378e308398662d5180adfda0689e37e081736200',
            u'RepoTags': [u'gluuopendj:latest'],
            u'Size': 0,
            u'VirtualSize': 260371028}]
            or
            []
        """
        if not image:
            run('mkdir /tmp/{}'.format(args.node_type))
            raw_url = 'https://raw.githubusercontent.com/GluuFederation/gluu-docker/master/ubuntu/14.04/{}/Dockerfile'.format(args.node_type)
            run('wget -q {} -P /tmp/{}'.format(raw_url, args.node_type))
            run('docker build -q --rm --force-rm -t {} {}'.format(args.node_type, '/tmp/{}'.format(args.node_type)))
            run('rm -rf /tmp/{}'.format(args.node_type))
        
        # deploy container
        con_name = '{0}_{1}_{2}'.format(args.node_type, args.cluster, randrange(101,999))
        cid = run('docker run -d -P --name={0} {1}'.format(con_name, args.node_type))
        scid = cid.strip()[:-(len(cid)-12)]
        # accept container cert in host salt-master
        sleep(10)
        run('salt-key -y -a {}'.format(scid))
        # create ldapNode() object
        node = get_node_object(args.node_type)
        # populate ldapNode object
        node.id = scid
        node.name = con_name
        node.type = args.node_type
        # run setup using salt
        node.setup()
        # add ldapNode object into cluster object
        cluster.add_node(node)
        # save cluster object in db
        cluster.persist()
        return {'status_code': 201, 'message': '{} node created in Cluster: {}'.format(args.node_type, args.cluster)}

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
