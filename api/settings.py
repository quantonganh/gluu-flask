# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('API_SECRET', 'blablabla')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    # CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    PORT = 8080
    DATA_DIR = os.path.expanduser('~') + '/gfdata'
    CLUSTER_FILE = DATA_DIR + '/cluster.json'
    DB = os.path.join(PROJECT_ROOT, "db")


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    RELOADER = False


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    DB = os.path.join(Config.PROJECT_ROOT, "dbtest")
