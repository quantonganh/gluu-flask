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

from .base import BaseModel


@swagger.model
class GluuCluster(BaseModel):
    __table_name__ = "clusters"

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
        'encoded_ox_ldap_pw': fields.String,
        'encoded_ldap_pw': fields.String,
        'oxauthClient_encoded_pw': fields.String,
        'baseInum': fields.String(attribute='Unique identifier for domain'),
        'inumOrg': fields.String(attribute='Unique identifier for organization'),  # noqa
        'inumOrgFN': fields.String(attribute='Unique organization identifier sans special characters.'),  # noqa
        'inumAppliance': fields.String(attribute='Unique identifier for cluster'),  # noqa
        'inumApplianceFN': fields.String(attribute='Unique cluster identifier sans special characters.')  # noqa
    }
    required = ['id']

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
        self.orgName = None
        self.orgShortName = None
        self.countryCode = None
        self.city = None
        self.state = None
        self.admin_email = None

        # Cluster secrets
        self.encoded_ox_ldap_pw = None
        self.encoded_ldap_pw = None
        self.oxauthClient_encoded_pw = None

        # Inums
        self.baseInum = None
        self.inumOrg = None
        self.inumAppliance = None
        self.inumOrgFN = None
        self.inumApplianceFN = None

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
        if node_type not in self.available_node_types:
            raise ValueError("{!r} node is not supported".format(node_type))

        node_container = self.node_type_map.get(node_type)
        node_container.append(node.id)

    def remove_node(self, node):
        node_type = getattr(node, "type")
        if node_type not in self.available_node_types:
            raise ValueError("{!r} node is not supported".format(node_type))
        node_container = self.node_type_map.get(node_type)
        node_container.remove(node.id)

    @property
    def available_node_types(self):
        return tuple(self.node_type_map.keys())

    @property
    def node_type_map(self):
        node_type_map = {
            "gluuopendj": self.ldap_nodes,
            "oxauth": self.oxauth_nodes,
            "oxtrust": self.oxtrust_nodes,
        }
        return node_type_map
