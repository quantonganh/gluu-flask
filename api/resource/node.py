# -*- coding: utf-8 -*-
'''/node resource'''
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from ..model import ldapNode
from flask import g
from flask.ext.restful import reqparse
import subprocess
import sys

def run(command, exit_on_error=True, cwd=None):
        try:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, cwd=cwd)
        except subprocess.CalledProcessError, e:
            if exit_on_error:
                sys.exit(e.returncode)
            else:
                raise

def get_image(name = ''):
    from docker import Client
    c = Client(base_url='unix://var/run/docker.sock')
    return c.images(name)

class Node(Resource):
    """
    Node is a docker container runs salt-minions and points to salt-master
    Create gluu node
    """
    images = ['saltminion', 'gluuopendj', 'gluuoxauth', 'gluuoxtrust', 'gluuhttpd', 'gluushib', 'gluuasimba', 'gluucas']

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
        parameters = [],
        responseMessages=[
            {
              "code": 200,
              "message": "node created"
            }
          ],
        summary = 'TODO'
        )
    def post(self):
        #post data: {"cluster":"id/name","node":"gluuopendj"}
        post_parser = reqparse.RequestParser()
        post_parser.add_argument(
            'cluster', type=str, location='form',
            required=True, help='Cluster name or id',
        )
        post_parser.add_argument(
            'node_type', type=str, location='form',
            required=True, help='node type: ldap | oxauth | oxtrust',
        )
        args = post_parser.parse_args()
        # check that cluster name or id is valid else return with message and code
        if args.cluster not in ['1234', 'gluu']:
            return {'echo': 'cluster not found'}

        # get relivent dockerfile
        # build image
        image = get_image(args.node_type)
        """
            [{u'Created': 1422048669,
            u'Id': u'e348da14b96d85f1dfec380b53dfb106ea1fb4723f93fa8619ad798fd9509f7c',
            u'ParentId': u'26bc41e2ffeec6cff2d1880f378e308398662d5180adfda0689e37e081736200',
            u'RepoTags': [u'saltminion:latest'],
            u'Size': 0,
            u'VirtualSize': 260371028}]
            or
            []
        """
        if not image and args.node in images:
            run('mkdir /tmp/{}'.format(args.node))
            raw_url = 'https://raw.githubusercontent.com/GluuFederation/gluu-docker/master/ubuntu/14.04/{}/Dockerfile'.format(args.node)
            run('wget -q {} -P /tmp/{}'.format(raw_url, args.node))
            run('docker build -q --rm --force-rm -t {} {}'.format(args.node, '/tmp/{}'.format(args.node)))
            run('rm -rf /tmp/{}'.format(args.node))
        else:
            return {'echo': 'requested node is unknown'}
        
        # deploy container
        # accept container cert in host salt-master
        # create ldapNode() object
        # populate ldapNode object
        # add ldapNode object into cluster object
        # save cluster object in db
        return {'echo': '{} node created in Cluster: {}'.format(args.node, args.cluster)}

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
