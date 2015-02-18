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

import salt.client
from flask_restful_swagger import swagger
from flask.ext.restful import fields

from .base import BaseModel


@swagger.model
class ldapNode(BaseModel):
    __table_name__ = "nodes"

    # Swager Doc
    resource_fields = {
        'id': fields.String(attribute='Node unique identifier'),
        'type': fields.String(attribute='Node type'),
        'cluster_id': fields.String(attribute='Cluster ID'),
        'local_hostname': fields.String(attribute='Local hostname of the node (not the cluster hostname).'),
        'ip': fields.String(attribute='IP address of the node'),
        'ldap_setup_properties': fields.String(attribute='Filesystem path of the opendj-setup.properties template'),
        'openDjCertFn': fields.String(attribute='Filesystem path of the public certificate for OpenDJ'),
        'ldap_binddn': fields.String(attribute='LDAP super user Bind DN. Probably should leave it default cn=directory manager.'),
        'ldap_port': fields.String(attribute='Non SSL LDAP port (not used)'),
        'ldaps_port': fields.String(attribute='LDAPS port'),
        'ldap_admin_port': fields.String(attribute='Admin port'),
        'ldap_jmx_port': fields.String(attribute='JMX port (not used)'),
        'ldapBaseFolder': fields.String(attribute='Where to install OpenDJ, usually /opt/opendj'),
        'ldapStartTimeOut': fields.String(attribute='How long to wait for LDAP to start.'),
        'ldapSetupCommand': fields.String(attribute='Full path to opendj setup command'),
        'ldapDsconfigCommand': fields.String(attribute='Full path to dsconfig command'),
        'ldapDsCreateRcCommand': fields.String(attribute='Full path to create-rc command'),
        'ldapDsJavaPropCommand': fields.String(attribute='Full path to dsjavaproperties command'),
        'importLdifCommand': fields.String(attribute='Full path to import command'),
        'ldapEncodePWCommand': fields.String(attribute='Full path to encode password'),
        'ldapPassFn': fields.String(attribute='Temporary path to store ldap password (should be removed)'),
        'schemaFolder': fields.String(attribute='Full path of template schema to copy to the opendj server'),
        'init_file': fields.String(attribute='Full path of tempalte init file'),
        'ldap_start_script': fields.String(attribute='Full path of the destination of the init script'),
        'keytoolCommand': fields.String(attribute='Full path to java keytool command'),
        'opensslCommand': fields.String(attribute='Full path to openssl command'),
        'ldif_base': fields.String(attribute='Full path to output folder ldif'),
        'ldif_appliance': fields.String(attribute='Full path to output folder ldif'),
        'ldif_attributes': fields.String(attribute='Full path to output folder ldif'),
        'ldif_scopes': fields.String(attribute='Full path to output folder ldif'),
        'ldif_clients': fields.String(attribute='Full path to output folder ldif'),
        'ldif_people': fields.String(attribute='Full path to output folder ldif'),
        'ldif_groups': fields.String(attribute='Full path to output folder ldif'),
        'ldif_site': fields.String(attribute='Full path to output folder ldif'),
        'ldif_scripts': fields.String(attribute='Full path to output folder ldif'),
        'ldif_files': fields.List(fields.String, attribute='List of initial ldif files')
        }

    def __init__(self, install_dir=None):
        self.install_dir = install_dir
        self.outputFolder = ""
        self.ldap_type = ""

        self.local_hostname = None
        self.ip = None
        self.ldap_setup_properties = './templates/opendj-setup.properties'
        self.openDjCertFn = '/etc/certs/opendj.crt'
        self.ldap_binddn = 'cn=directory manager'
        self.ldap_port = '1389'
        self.ldaps_port = '1636'
        self.ldap_jmx_port = '1689'
        self.ldap_admin_port = '4444'
        self.ldapBaseFolder = '/opt/opendj'
        self.ldapStartTimeOut = 30
        self.ldapSetupCommand = '%s/setup' % self.ldapBaseFolder
        self.ldapDsconfigCommand = "%s/bin/dsconfig" % self.ldapBaseFolder
        self.ldapDsCreateRcCommand = "%s/bin/create-rc-script" % self.ldapBaseFolder
        self.ldapDsJavaPropCommand = "%s/bin/dsjavaproperties" % self.ldapBaseFolder
        self.importLdifCommand = '%s/bin/import-ldif' % self.ldapBaseFolder
        self.ldapEncodePWCommand = '%s/bin/encode-password' % self.ldapBaseFolder
        self.ldapPassFn = '/home/ldap/.pw'
        self.schemaFolder = "%s/template/config/schema" % self.ldapBaseFolder
        self.org_custom_schema = "%s/config/schema/100-user.ldif" % self.ldapBaseFolder
        self.schemaFiles = ["%s/static/%s/96-eduperson.ldif" % (self.install_dir, self.ldap_type),
                            "%s/static/%s/101-ox.ldif" % (self.install_dir, self.ldap_type),
                            "%s/static/%s/77-customAttributes.ldif" % (self.install_dir, self.ldap_type),
                            "%s/output/100-user.ldif" % self.install_dir]
        self.init_file = '%s/static/opendj/opendj' % self.install_dir
        self.ldap_start_script = '/etc/init.d/opendj'

        self.keytoolCommand = '/usr/java/latest/bin/keytool'
        self.opensslCommand = '/usr/bin/openssl'

        self.ldif_base = '%s/base.ldif' % self.outputFolder
        self.ldif_appliance = '%s/appliance.ldif' % self.outputFolder
        self.ldif_attributes = '%s/attributes.ldif' % self.outputFolder
        self.ldif_scopes = '%s/scopes.ldif' % self.outputFolder
        self.ldif_clients = '%s/clients.ldif' % self.outputFolder
        self.ldif_people = '%s/people.ldif' % self.outputFolder
        self.ldif_groups = '%s/groups.ldif' % self.outputFolder
        self.ldif_site = '%s/static/cache-refresh/o_site.ldif' % self.install_dir
        self.ldif_scripts = '%s/scripts.ldif' % self.outputFolder
        self.ldif_files = [self.ldif_base,
                           self.ldif_appliance,
                           self.ldif_attributes,
                           self.ldif_scopes,
                           self.ldif_clients,
                           self.ldif_people,
                           self.ldif_groups,
                           self.ldif_site,
                           self.ldif_scripts]

    def setup(self):
        saltlocal = salt.client.LocalClient()
        with open(self.ldapPassFn, 'w') as fp:
            f.write(self.ldapPass)
        for ldif in self.ldif_files:
            with open(ldif, 'r') as fp:
                tmpl = fp.read()
            with open('/tmp/'+ldif, 'w') as fp:
                fp.write(tmpl % self.__dict__)
            #saltlocal.cmd(self.id, 'cmd.run', ['uname -a'])
            saltlocal.cmd(self.id, 'cp.get_file', ['/tmp/'+ldif, target])
