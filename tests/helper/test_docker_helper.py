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
