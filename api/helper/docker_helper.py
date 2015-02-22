# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014 Gluu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os.path
import tempfile

import docker.errors
import requests
from docker import Client
from crochet import run_in_reactor

docker_client = Client(base_url="unix://var/run/docker.sock")


def image_exists(name):
    """Checks whether a docker image exists.

    :param name: Image name
    :returns: ``True`` if image exists, otherwise ``False``
    """
    images = docker_client.images(name)
    return True if images else False


def build_image(path, tag):
    """Builds a docker image.

    :param path: Path to a directory where ``Dockerfile`` is located.
    :param tag: Desired tag name.
    """
    resp = docker_client.build(path, tag=tag, quiet=True,
                               rm=True, forcerm=True, pull=False)

    output = ""
    while True:
        try:
            output = resp.next()
            # TODO: use proper logging
            print(output)
        except StopIteration:
            break

    result = json.loads(output)
    if "errorDetail" in result:
        return False
    return True


def run_container(name, image):
    """Runs a docker container in detached mode.

    This is a two-steps operation:

    1. Creates container
    2. Starts container

    :param name: Desired container name.
    :param image: Existing image name.
    :returns: A string of container ID in long format if container
              is running successfully, otherwise an empty string.
    """
    container_id = ""

    try:
        container = docker_client.create_container(image=image, name=name,
                                                   detach=True, command=[])
        container_id = container["Id"]
    except docker.errors.APIError as exc:
        # TODO: handles error by status code
        err_code = exc.response.status_code
        if err_code == 409:
            # container exists
            pass
        elif err_code == 404:
            # container doesn't exist
            pass

    if container_id:
        docker_client.start(container=container_id, publish_all_ports=True)
    return container_id


def get_remote_files(*files):
    """Retrieves files from remote paths.

    All retrieved files will be stored under a same temporary directory.
    """
    local_dir = tempfile.mkdtemp()

    for file_ in files:
        local_path = os.path.join(local_dir, os.path.basename(file_))
        resp = requests.get(file_)
        if resp.status_code == 200:
            with open(local_path, "w") as fp:
                fp.write(resp.text)
    return local_dir


def _build_saltminion():
    """Builds saltminion image.
    """
    build_succeed = True

    if not image_exists("saltminion"):
        minion_file = "https://raw.githubusercontent.com/GluuFederation" \
                      "/gluu-docker/master/ubuntu/14.04/saltminion/minion"
        dockerfile = "https://raw.githubusercontent.com/GluuFederation" \
                     "/gluu-docker/master/ubuntu/14.04/saltminion/Dockerfile"
        files = [minion_file, dockerfile]
        build_dir = get_remote_files(*files)
        build_succeed = build_image(build_dir, "saltminion")
    return build_succeed


@run_in_reactor
def setup_container(name, image, dockerfile):
    """Builds and runs a container.

    :param name: Container name.
    :param image: Image name.
    :param dockerfile: Path to remote Dockerfile. Used to build the image
                       if image is not exist.
    :returns: Container ID in long format if container running successfully,
              otherwise an empty string.
    """
    # saltminion image is required
    if not _build_saltminion():
        return ""

    # a flag to determine whether build image process is succeed
    build_succeed = True

    if not image_exists(image):
        build_dir = get_remote_files(dockerfile)
        build_succeed = build_image(build_dir, image)

    if build_succeed:
        return run_container(name, image)
    return ""
