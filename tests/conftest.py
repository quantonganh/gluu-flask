import uuid
import os

import pytest


@pytest.fixture(scope="session")
def config():
    from api.settings import TestConfig
    return TestConfig


@pytest.fixture(scope="session")
def app(request):
    from api.app import create_app
    from api.settings import TestConfig

    app = create_app(TestConfig)
    return app


@pytest.fixture()
def db(request, app):
    from api.database import db

    db.init_app(app)

    def teardown():
        os.unlink(app.config["DATABASE_URI"])

    request.addfinalizer(teardown)
    return db


@pytest.fixture()
def cluster():
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    return cluster


@pytest.fixture()
def ldap_node(cluster):
    from api.model import ldapNode

    node = ldapNode()
    node.id = "{}".format(uuid.uuid4())
    node.type = "ldap"
    node.cluster_id = cluster.id
    return node


@pytest.fixture()
def oxauth_node(cluster):
    from api.model import ldapNode

    node = ldapNode()
    node.id = "{}".format(uuid.uuid4())
    node.type = "oxauth"
    node.cluster_id = cluster.id
    return node


@pytest.fixture()
def oxtrust_node(cluster):
    from api.model import ldapNode

    node = ldapNode()
    node.id = "{}".format(uuid.uuid4())
    node.type = "oxtrust"
    node.cluster_id = cluster.id
    return node
