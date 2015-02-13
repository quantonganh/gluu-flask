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
        import shutil
        shutil.rmtree(app.config["DB"])

    request.addfinalizer(teardown)
    return app
