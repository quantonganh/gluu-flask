import pytest


@pytest.fixture(scope="session")
def docker_helper(request):
    from api.helper.docker_helper import DockerHelper

    helper = DockerHelper()

    def teardown():
        helper.docker.close()

    request.addfinalizer(teardown)
    return helper
