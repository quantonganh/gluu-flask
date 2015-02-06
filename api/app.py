# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask
from api.settings import ProdConfig
from api.extensions import (
    restapi,
)
from api.resource.node import Node
from api.resource.cluster import Cluster


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_resources()
    register_extensions(app)
    #register_blueprints(app)
    return app


def register_extensions(app):
    restapi.init_app(app)
    return None

def register_resources():
    restapi.add_resource(Node, '/node/<string:node_id>')
    restapi.add_resource(Cluster, '/cluster/<string:cluster_id>')
    return None

def register_blueprints(app):
    return None
