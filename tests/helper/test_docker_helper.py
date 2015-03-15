def test_image_exists_found(monkeypatch, docker_helper):
    # stubbed ``docker.Client.images`` method's return value
    monkeypatch.setattr(
        "docker.Client.images",
        lambda cls, name: [
            {
                'Created': 1401926735,
                'Id': 'a9eb172552348a9a49180694790b33a1097f546456d041b6e82e4d',
                'ParentId': '120e218dd395ec314e7b6249f39d2853911b3d6def6ea164',
                'RepoTags': ['busybox:buildroot-2014.02', 'busybox:latest'],
                'Size': 0,
                'VirtualSize': 2433303,
            }
        ],
    )
    assert docker_helper.image_exists("busybox") is True


def test_image_exists_notfound(monkeypatch, docker_helper):
    # stubbed ``docker.Client.images`` method's return value
    monkeypatch.setattr("docker.Client.images", lambda cls, name: [])
    assert docker_helper.image_exists("busybox") is False


def test_get_container_ip(monkeypatch, docker_helper):
    ipaddr = "172.17.0.4"

    monkeypatch.setattr(
        "docker.Client.inspect_container",
        lambda cls, container: {"NetworkSettings": {"IPAddress": ipaddr}},
    )
    assert docker_helper.get_container_ip("abc") == ipaddr


def test_build_image_success(monkeypatch, docker_helper):
    stream_output = [
        '{"stream":" ---\\u003e a9eb17255234\\n"}',
        '{"stream":"Successfully built 032b8b2855fc\\n"}'
    ]

    def gen(stream_output):
        for output in stream_output:
            yield output

    monkeypatch.setattr(
        "docker.Client.build",
        lambda cls, path, tag, quiet, rm, forcerm, pull: gen(stream_output),
    )
    assert docker_helper.build_image("/tmp/abc", "abc") is True


def test_build_image_failed(monkeypatch, docker_helper):
    stream_output = [
        '{"stream":" ---\\u003e a9eb17255234\\n"}',
        '{"errorDetail": {}}'
    ]

    def gen(stream_output):
        for output in stream_output:
            yield output

    monkeypatch.setattr(
        "docker.Client.build",
        lambda cls, path, tag, quiet, rm, forcerm, pull: gen(stream_output),
    )
    assert docker_helper.build_image("/tmp/abc", "abc") is False


def test_run_container(monkeypatch, docker_helper):
    monkeypatch.setattr(
        "docker.Client.create_container",
        lambda cls, image, name, detach, command, environment: {"Id": "123"},
    )
    monkeypatch.setattr(
        "docker.Client.start",
        lambda cls, container, publish_all_ports: "",
    )
    assert docker_helper.run_container("abc", "gluuopendj") == "123"


def test_build_saltminion(monkeypatch, docker_helper):
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.image_exists",
        lambda cls, name: [{
            'Created': 1401926735,
            'Id': 'a9eb172552348a9a49180694790b33a1097f546456d041b6e82e4d',
            'ParentId': '120e218dd395ec314e7b6249f39d2853911b3d6def6ea164',
            'RepoTags': ['saltminion:latest'],
            'Size': 0,
            'VirtualSize': 2433303,
        }],
    )
    assert docker_helper._build_saltminion() is True


def test_build_saltminion_no_image(monkeypatch, docker_helper):
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.image_exists",
        lambda cls, name: [],
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.get_remote_files",
        lambda cls, *files: "/tmp/gluuopendj",
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.build_image",
        lambda cls, path, tag: True,
    )
    # not sure whether to monkeypatch of use fixture
    monkeypatch.setattr("shutil.rmtree", lambda path: None)
    assert docker_helper._build_saltminion() is True


def test_setup_container_existing_image(monkeypatch, docker_helper):
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper._build_saltminion",
        lambda cls: True,
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.image_exists",
        lambda cls, name: [{
            'Created': 1401926735,
            'Id': 'a9eb172552348a9a49180694790b33a1097f546456d041b6e82e4d',
            'ParentId': '120e218dd395ec314e7b6249f39d2853911b3d6def6ea164',
            'RepoTags': ['gluuopendj:latest'],
            'Size': 0,
            'VirtualSize': 2433303,
        }],
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.run_container",
        lambda cls, name, image: "123",
    )

    container_id = docker_helper.setup_container(
        "gluuopendj_123", "gluuopendj",
        "http://example.com/Dockerfile", "127.0.0.1",
    )
    assert container_id == "123"


def test_setup_container_no_saltminion(monkeypatch, docker_helper):
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper._build_saltminion",
        lambda cls: False,
    )
    container_id = docker_helper.setup_container(
        "gluuopendj_123", "gluuopendj",
        "http://example.com/Dockerfile", "127.0.0.1",
    )
    assert container_id == ""


def test_setup_container_failed(monkeypatch, docker_helper):
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper._build_saltminion",
        lambda cls: True,
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.image_exists",
        lambda cls, name: [],
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.get_remote_files",
        lambda cls, *files: "/tmp/gluuopendj",
    )
    monkeypatch.setattr(
        "api.helper.docker_helper.DockerHelper.build_image",
        lambda cls, path, tag: False,
    )
    # not sure whether to monkeypatch of use fixture
    monkeypatch.setattr("shutil.rmtree", lambda path: None)

    container_id = docker_helper.setup_container(
        "gluuopendj_123", "gluuopendj",
        "http://example.com/Dockerfile", "127.0.0.1",
    )
    assert container_id == ""
