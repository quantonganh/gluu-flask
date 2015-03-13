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
    DATABASE_URI = os.path.join(DATA_DIR, "db", "db.json")
    SALT_MASTER_IPADDR = os_env.get("SALT_MASTER_IPADDR", "")
    # Is there any better place to put this path
    #DOCKER_REPO = 'https://raw.githubusercontent.com/GluuFederation/gluu-docker/master/ubuntu/14.04'


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    RELOADER = False
    DATABASE_URI = os.path.join(Config.PROJECT_ROOT, "db", "db_dev.json")


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    DB = os.path.join(Config.PROJECT_ROOT, "dbtest")
    DATABASE_URI = os.path.join(Config.PROJECT_ROOT, "db", "db_test.json")
