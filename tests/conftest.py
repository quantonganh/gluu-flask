import os.path
import shutil
import uuid

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

    def teardown():
        shutil.rmtree(app.config["DB"])

    request.addfinalizer(teardown)
    return app


@pytest.fixture()
def cluster(request, config):
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    cluster.persist(config.DB)

    def teardown():
        fp = os.path.join(config.DB, "cluster_{}.json".format(cluster.id))
        try:
            os.unlink(fp)
        except OSError as exc:
            # likely file has been removed
            if exc.errno == 2:
                pass

    request.addfinalizer(teardown)
    return cluster
