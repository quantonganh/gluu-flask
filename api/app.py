# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask
from api.settings import ProdConfig
from api.extensions import (
    restapi,
)
from api.resource.node import Node
from api.resource.node import NodeList
from api.resource.cluster import Cluster
from api.resource.cluster import ClusterList
from api.database import db


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_resources()
    register_extensions(app)
    return app


def register_extensions(app):
    restapi.init_app(app)
    db.init_app(app)


def register_resources():
    restapi.add_resource(NodeList, '/node')
    restapi.add_resource(Node, '/node/<string:node_id>')
    restapi.add_resource(ClusterList, '/cluster')
    restapi.add_resource(Cluster, '/cluster/<string:cluster_id>')
