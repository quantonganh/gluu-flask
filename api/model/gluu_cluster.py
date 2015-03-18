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
from flask_restful_swagger import swagger
from flask.ext.restful import fields

from api.model.base import BaseModel
from api.helper.common_helper import get_quad


@swagger.model
class GluuCluster(BaseModel):
    # Swager Doc
    resource_fields = {
        'id': fields.String(attribute='GluuCluster unique identifier'),
        'name': fields.String(attribute='GluuCluster name'),
        'description': fields.String(attribute='Description of cluster'),
        'ldap_nodes': fields.List(fields.String, attribute='Ids of ldap nodes'),  # noqa
        'oxauth_nodes': fields.List(fields.String, attribute='Ids of oxauth nodes'),  # noqa
        'oxtrust_nodes': fields.List(fields.String, attribute='Ids of oxtrust nodes'),  # noqa
        'hostname_ldap_cluster': fields.String,
        'hostname_oxauth_cluster': fields.String,
        'hostname_oxtrust_cluster': fields.String,
        'ldaps_port': fields.String,
        'orgName': fields.String(attribute='Name of org for X.509 certificate'),  # noqa
        'orgShortName': fields.String(attribute='Short name of org for X.509 certificate'),  # noqa
        'countryCode': fields.String(attribute='ISO 3166-1 alpha-2 country code'),  # noqa
        'city': fields.String(attribute='City for X.509 certificate'),
        'state': fields.String(attribute='State or province for X.509 certificate'),  # noqa
        'admin_email': fields.String(attribute='Admin email address for X.509 certificate'),  # noqa
        'encrypted_pw': fields.String(attribute='Secret for ldap cn=directory manager, and oxTrust admin'),
        'ldap_replication_admin_pw': fields.String(attribute='Password for LDAP replication admin'),
        'baseInum': fields.String(attribute='Unique identifier for domain'),
        'inumOrg': fields.String(attribute='Unique identifier for organization'),  # noqa
        'inumOrgFN': fields.String(attribute='Unique organization identifier sans special characters.'),  # noqa
        'inumAppliance': fields.String(attribute='Unique identifier for cluster'),  # noqa
        'inumApplianceFN': fields.String(attribute='Unique cluster identifier sans special characters.'),  # noqa
    }

    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""
        self.ldap_nodes = []
        self.oxauth_nodes = []
        self.oxtrust_nodes = []
        self.hostname_ldap_cluster = ""
        self.hostname_oxauth_cluster = ""
        self.hostname_oxtrust_cluster = ""
        self.ldaps_port = "1636"

        # X.509 Certificate Information
        self.orgName = ""
        self.orgShortName = ""
        self.countryCode = ""
        self.city = ""
        self.state = ""
        self.admin_email = ""

        # Secret for ldap cn=directory manager, and oxTrust admin
        self.encrypted_pw = ""

        # Password for LDAP replication admin
        self.ldap_replication_admin_pw = ""

        # Inums
        self.baseInum = '@!%s.%s.%s.%s' % tuple([get_quad() for i in xrange(4)])

        org_quads = '%s.%s' % tuple([get_quad() for i in xrange(2)])
        self.inumOrg = '%s!0001!%s' % (self.baseInum, org_quads)

        appliance_quads = '%s.%s' % tuple([get_quad() for i in xrange(2)])
        self.inumAppliance = '%s!0002!%s' % (self.baseInum, appliance_quads)

        self.inumOrgFN = self.inumOrg.replace('@', '').replace('!', '').replace('.', '')
        self.inumApplianceFN = self.inumAppliance.replace('@', '').replace('!', '').replace('.', '')

    def add_node(self, node):
        """Adds node into current cluster.

        ``Node.type`` determines where to put the node to.
        For example, node with ``ldap`` type will be appended to
        ``GluuCluster.ldap_nodes``.

        List of supported node types:

        * ``ldap``
        * ``oxauth``
        * ``oxtrust``

        :param node: an instance of any supported Node class.
        """
        node_type = getattr(node, "type")
        node_attr = self.node_type_map.get(node_type)
        if node_attr is None:
            raise ValueError("{!r} node is not supported".format(node_type))
        node_attr.append(node.id)

    def remove_node(self, node):
        """Removes node from current cluster.

        ``Node.type`` determines where to remove the node from.
        For example, node with ``ldap`` type will be removed from
        ``GluuCluster.ldap_nodes``.

        List of supported node types:

        * ``ldap``
        * ``oxauth``
        * ``oxtrust``

        :param node: an instance of any supported Node class.
        """
        node_type = getattr(node, "type")
        node_attr = self.node_type_map.get(node_type)
        if node_attr is None:
            raise ValueError("{!r} node is not supported".format(node_type))
        node_attr.remove(node.id)

    @property
    def node_type_map(self):
        node_type_map = {
            "ldap": self.ldap_nodes,
            "oxauth": self.oxauth_nodes,
            "oxtrust": self.oxtrust_nodes,
        }
        return node_type_map

    def set_fields(self, data=None):
        data = data or {}
        for attr, val in data.items():
            # skip field that is None
            if val is None:
                continue
            setattr(self, attr, val)
