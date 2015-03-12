# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Gluu
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
import tempfile
import time
from random import randrange

from crochet import run_in_reactor

from api.database import db
from api.model import ldapNode
from api.model import oxauthNode
from api.model import oxtrustNode  # noqa
from api.helper.docker_helper import DockerHelper
from api.helper.salt_helper import register_minion
from api.helper.common_helper import get_random_chars
from api.helper.common_helper import run
from api.setup.ldap_setup import ldapSetup
from api.setup.oxauth_setup import OxAuthSetup
from api.log import create_file_logger


class LdapModelHelper(object):
    def __init__(self, cluster, salt_master_ipaddr):
        self.salt_master_ipaddr = salt_master_ipaddr
        self.cluster = cluster
        self.node = ldapNode()
        self.node.cluster_id = cluster.id
        self.node.type = "ldap"
        # TODO: encode password
        self.node.ldapPass = get_random_chars()
        self.node.name = "{}_{}_{}".format(self.image, self.cluster.id,
                                           randrange(101, 999))

        _, self.logpath = tempfile.mkstemp(suffix=".build.log",
                                           prefix=self.image + "-")
        self.logger = create_file_logger(self.logpath)
        self.docker = DockerHelper(logger=self.logger)

    @property
    def image(self):
        return "gluuopendj"

    @property
    def dockerfile(self):
        return "https://raw.githubusercontent.com/GluuFederation" \
               "/gluu-docker/master/ubuntu/14.04/gluuopendj/Dockerfile"

    @property
    def name(self):
        return self.node.name

    @run_in_reactor
    def setup_node(self):
        # TODO - This should be in a try/except, with logging for
        # both creation and errors to access log, and just errors
        # to error log.
        cont_id = self.docker.setup_container(
            self.name, self.image, self.dockerfile, self.salt_master_ipaddr)

        if cont_id:
            # container ID in short format
            self.node.id = cont_id[:12]

            # wait for 10 seconds to make sure minion connected
            # and sent its key to master

            # There must be a way around this
            print "Sleeping for 10 seconds"
            time.sleep(10)

            # register the container as minion
            register_minion(self.node.id)
            container_ip = self.docker.get_container_ip(self.node.id)

            self.node.local_hostname = container_ip
            self.node.ip = container_ip

            # delay the remote execution
            # see https://github.com/saltstack/salt/issues/13561

            # There must be a way around this
            print "Sleeping for 15 seconds"
            time.sleep(15)
            print "Continuing"
            ldap_setup = ldapSetup(self.node, self.cluster, self.logger)
            ldap_setup.setup()

            db.persist(self.node, "nodes")
            self.cluster.add_node(self.node)
            db.update(self.cluster.id, self.cluster, "clusters")


def stop_ldap(node):
    try:
        run("salt {} cmd.run '{}/bin/stop-ds'".format(node.id, node.ldapBaseFolder))
    except SystemExit as exc:
        if exc.code == 2:
            # executable may not exist or minion is unreachable
            pass


class OxAuthModelHelper(object):
    setup_class = OxAuthSetup
    node_class = oxauthNode

    def __init__(self, cluster, salt_master_ipaddr):
        self.salt_master_ipaddr = salt_master_ipaddr
        self.cluster = cluster

        self.node = self.node_class()
        self.node.cluster_id = cluster.id
        self.node.name = "{}_{}_{}".format(self.image, self.cluster.id,
                                           randrange(101, 999))

        _, self.logpath = tempfile.mkstemp(
            suffix=".log", prefix=self.image + "-build-")
        self.logger = create_file_logger(self.logpath)
        self.docker = DockerHelper(logger=self.logger)

    @property
    def image(self):
        return "gluuoxauth"

    @property
    def dockerfile(self):
        return "https://raw.githubusercontent.com/GluuFederation" \
               "/gluu-docker/master/ubuntu/14.04/gluuoxauth/Dockerfile"

    @property
    def name(self):
        return self.node.name

    @run_in_reactor
    def setup(self):
        # runs callback before setup and continue if succeed
        if self.before_setup():
            setup_obj = self.setup_class(self.node, self.cluster, self.logger)

            # runs callback after setup succeed
            if setup_obj.setup():
                self.after_setup()

    def before_setup(self):
        container_id = self.docker.setup_container(
            self.name, self.image, self.dockerfile, self.salt_master_ipaddr)

        if not container_id:
            self.logger.error("Failed to start "
                              "the {!r} container".format(self.name))
            return False

        # container ID in short format
        self.node.id = container_id[:12]

        self.node.hostname = self.docker.get_container_ip(self.node.id)

        # wait for 10 seconds to make sure minion connected
        # and sent its key to master
        # TODO: there must be a way around this
        self.logger.info("Waiting for minion to connect; "
                         "sleeping for 10 seconds")
        time.sleep(10)

        # FIXME: gluuoxauth container stopped after it has been created
        # register the container as minion
        if not register_minion(self.node.id):
            self.logger.error("Stopping; unable to find minion {!r}".format(self.node.id))
            return False

        # delay the remote execution
        # see https://github.com/saltstack/salt/issues/13561
        # TODO: there must be a way around this
        self.logger.info("Preparing remote execution; sleeping for 15 seconds")
        time.sleep(15)
        return True

    def after_setup(self):
        db.persist(self.node, "nodes")
        self.cluster.add_node(self.node)
        db.update(self.cluster.id, self.cluster, "clusters")
        return True
