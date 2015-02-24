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
from random import randrange

from crochet import run_in_reactor

from api.database import db
from api.model import ldapNode
from api.model import oxauthNode  # noqa
from api.model import oxtrustNode  # noqa
from api.helper.docker_helper import setup_container
from api.helper.salt_helper import register_minion


class LdapModelHelper(object):
    def __init__(self, cluster):
        self.cluster = cluster
        self.node = ldapNode()
        self.node.cluster_id = cluster.id
        self.node.type = "ldap"
        self.node.name = "{}_{}_{}".format(self.image, self.cluster.id,
                                           randrange(101, 999))

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
        # TODO - This should be in a try/except, with logging for both creation and errors to access log, and just errors to error log.
        cont_id = setup_container(self.name, self.image, self.dockerfile)
        if cont_id:
            self.node.id = cont_id[:-(len(cont_id) - 12)]
            register_minion(self.node.id)

            db.persist(self.node, "nodes")
            self.cluster.add_node(self.node)
            db.update(self.cluster.id, self.cluster, "clusters")
