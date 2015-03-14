import pytest


@pytest.fixture(scope="session")
def docker_helper(request, app):
    from api.helper.docker_helper import DockerHelper

    helper = DockerHelper(base_url=app.config["DOCKER_SOCKET"])

    def teardown():
        helper.docker.close()

    request.addfinalizer(teardown)
    return helper
