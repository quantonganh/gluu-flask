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
from api.model import oxtrustNode
from api.helper.docker_helper import DockerHelper
from api.helper.salt_helper import SaltHelper
# from api.helper.common_helper import encrypt_password
# from api.helper.common_helper import generate_passkey
from api.helper.common_helper import get_random_chars
from api.helper.common_helper import ox_encode_password
from api.helper.common_helper import run
from api.helper.common_helper import get_quad
from api.setup.ldap_setup import ldapSetup
from api.setup.oxauth_setup import OxAuthSetup
from api.setup.oxtrust_setup import OxTrustSetup
from api.log import create_file_logger


class BaseModelHelper(object):
    #: Node setup class. Must be overriden in subclass.
    setup_class = None

    #: Node model class. Must be overriden in subclass.
    node_class = None

    #: Docker image name. Must be overriden in subclass.
    image = ""

    #: URL to image's Dockerfile. Must be overriden in subclass.
    dockerfile = ""

    def __init__(self, cluster, salt_master_ipaddr, docker_base_url=""):
        assert self.setup_class, "setup_class must be set"
        assert self.node_class, "node_class must be set"
        assert self.image, "image attribute cannot be empty"
        assert self.dockerfile, "dockerfile attribute cannot be empty"

        self.salt_master_ipaddr = salt_master_ipaddr
        self.cluster = cluster

        self.node = self.node_class()
        self.node.cluster_id = cluster.id
        self.node.name = "{}_{}_{}".format(self.image, self.cluster.id,
                                           randrange(101, 999))

        _, self.logpath = tempfile.mkstemp(
            suffix=".log", prefix=self.image + "-build-")
        self.logger = create_file_logger(self.logpath, name=self.node.name)
        self.docker = DockerHelper(logger=self.logger, base_url=docker_base_url)
        self.salt = SaltHelper()

    def prepare_node_attrs(self):
        """Prepares changes to node's attributes (if any).

        It's worth noting that changing ``id`` attribute in this method
        should be avoided.
        """
        pass

    def prepare_minion(self):
        """Waits for minion to connect before doing any remote execution.
        """
        # wait for 10 seconds to make sure minion connected
        # and sent its key to master
        # TODO: there must be a way around this
        self.logger.info("Waiting for minion to connect; "
                         "sleeping for 10 seconds")
        time.sleep(10)

        # register the container as minion
        self.salt.register_minion(self.node.id)

        # delay the remote execution
        # see https://github.com/saltstack/salt/issues/13561
        # TODO: there must be a way around this
        self.logger.info("Preparing remote execution; "
                         "sleeping for 15 seconds")
        time.sleep(15)

    def before_save(self):
        """Callback before saving to database.

        Typical usage is to remove or protect sensitive field such as
        password or secret.
        """
        pass

    def save(self):
        """Saves node and updates the cluster where node belongs to.
        """
        # Runs pre-save callback
        self.before_save()

        db.persist(self.node, "nodes")
        self.cluster.add_node(self.node)
        db.update(self.cluster.id, self.cluster, "clusters")

    @run_in_reactor
    def setup(self):
        """Runs the node setup.
        """
        try:
            container_id = self.docker.setup_container(
                self.node.name, self.image,
                self.dockerfile, self.salt_master_ipaddr,
            )

            if container_id:
                # container ID in short format
                self.node.id = container_id[:12]

                # runs callback to prepare node attributes;
                # warning: don't override node.id attribute!
                self.prepare_node_attrs()

                self.prepare_minion()
                if self.salt.is_minion_registered(self.node.id):
                    setup_obj = self.setup_class(self.node, self.cluster, self.logger)
                    if setup_obj.setup():
                        self.logger.info("saving to database")
                        self.save()
                    setup_obj.after_setup()

                # minion is not connected
                else:
                    self.logger.error("minion {} is unreachable".format(self.node.id))

            # container is not running
            else:
                self.logger.error("Failed to start the {!r} container".format(self.node.name))
        except Exception as exc:
            self.logger.error(exc)


class LdapModelHelper(BaseModelHelper):
    setup_class = ldapSetup
    node_class = ldapNode
    image = "gluuopendj"
    dockerfile = "https://raw.githubusercontent.com/GluuFederation" \
                 "/gluu-docker/master/ubuntu/14.04/gluuopendj/Dockerfile"

    def prepare_node_attrs(self):
        # For replication, you will need
        # to use the ip address of docker instance as hostname--not the cluster
        # ldap hostname. For the four ports (ldap, ldaps, admin, jmx),
        # try to use the default
        # ports unless they are already in use, at which point it should chose
        # a random port over 10,000. Note these ports will need to be
        # open between the ldap docker instances
        container_ip = self.docker.get_container_ip(self.node.id)
        self.node.local_hostname = container_ip
        self.node.ip = container_ip

        # random plain-text LDAP password
        # self.node.ldapPass = get_random_chars()
        # self.node.encoded_ldap_pw = encrypt_password(self.node.ldapPass)

        # key = "".join([get_random_chars(), get_random_chars()])
        # key = generate_passkey()
        self.node.encoded_ox_ldap_pw = ox_encode_password(self.node.ldapPass, self.node.passkey)

        client_quads = '%s.%s' % tuple([get_quad() for i in xrange(2)])
        self.node.oxauth_client_id = '%s!0008!%s' % (self.cluster.baseInum, client_quads)

        self.node.oxauth_client_pw = get_random_chars()
        self.node.oxauth_client_encoded_pw = ox_encode_password(self.node.oxauth_client_pw, self.node.passkey)

    def before_save(self):
        self.node.oxauth_client_pw = ""


def stop_ldap(node, cluster):
    try:
        # since LDAP nodes are replicated if there's more than 1 node,
        # we need to disable the replication agreement first before
        # before stopping the opendj server
        if len(cluster.ldap_nodes) > 1:
            disable_repl_cmd = " ".join([
                "{}/bin/dsreplication".format(node.ldapBaseFolder), "disable",
                "--hostname", node.local_hostname,
                "--port", node.ldap_admin_port,
                "--adminUID", "admin",
                "--adminPassword", cluster.decrypted_admin_pw,
                "-X", "-n", "--disableAll",
            ])
            run("salt {} cmd.run '{}'".format(node.id, disable_repl_cmd))
        run("salt {} cmd.run '{}/bin/stop-ds'".format(node.id, node.ldapBaseFolder))
    except SystemExit as exc:
        if exc.code == 2:
            # executable may not exist or minion is unreachable
            pass
        print(exc)


class OxAuthModelHelper(BaseModelHelper):
    setup_class = OxAuthSetup
    node_class = oxauthNode
    image = "gluuoxauth"
    dockerfile = "https://raw.githubusercontent.com/GluuFederation" \
                 "/gluu-docker/master/ubuntu/14.04/gluuoxauth/Dockerfile"

    def prepare_node_attrs(self):
        container_ip = self.docker.get_container_ip(self.node.id)
        self.node.hostname = container_ip
        self.node.ip = container_ip

        # random plain-text LDAP password
        # TODO: perhaps should be stored in cluster object instead
        self.node.ldapPass = get_random_chars()
        key = "".join([get_random_chars(), get_random_chars()])
        self.node.encoded_ox_ldap_pw = ox_encode_password(self.node.ldapPass, key)

    def before_save(self):
        # set LDAP plain-text password as empty before saving to database
        self.node.ldapPass = ""


class OxTrustModelHelper(BaseModelHelper):
    setup_class = OxTrustSetup
    node_class = oxtrustNode
    image = "gluuoxtrust"
    dockerfile = "https://raw.githubusercontent.com/GluuFederation" \
                 "/gluu-docker/master/ubuntu/14.04/gluuoxtrust/Dockerfile"

    def prepare_node_attrs(self):
        container_ip = self.docker.get_container_ip(self.node.id)
        self.node.hostname = container_ip
        self.node.ip = container_ip

        self.node.ldapPass = get_random_chars()
        key = "".join([get_random_chars(), get_random_chars()])
        self.node.encoded_ox_ldap_pw = ox_encode_password(self.node.ldapPass, key)

        self.node.oxauth_client_pw = get_random_chars()
        self.node.oxauth_client_encoded_pw = ox_encode_password(self.node.oxauth_client_pw, key)

        client_quads = '%s.%s' % tuple([get_quad() for i in xrange(2)])
        self.node.oxauth_client_id = '%s!0008!%s' % (self.cluster.baseInum, client_quads)

        self.node.shib_jks_pass = get_random_chars()
        self.node.encoded_shib_jks_pw = ox_encode_password(self.node.shib_jks_pass, key)

    def before_save(self):
        # set oxtrust plain-text password as empty before saving to database
        self.node.shib_jks_pass = ""
        self.node.ldapPass = ""
        self.node.oxauth_client_pw = ""
