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
import salt.client

class ldapSetup(object):
    def __init__(self, node = None):
        self.saltlocal = salt.client.LocalClient()
        self.node = node
        #saltlocal.cmd(self.id, 'cmd.run', [dsconfigCmd])
        #saltlocal.cmd(self.id, 'cp.get_file', [schemaFile, self.schemaFolder])

        
    def writeLdapPW(self):
        saltlocal.cmd(self.node.id, 'cmd.run', ['mkdir -p /home/ldap'])
        saltlocal.cmd(self.node.id, 'cmd.run', ['echo {0} > {1}'.format(self.node.ldapPass, self.node.ldapPassFn)])
        saltlocal.cmd(self.node.id, 'cmd.run', ['chown ldap:ldap {}'.format(self.node.ldapPassFn)])

    def deleteLdapPW(self):
        saltlocal.cmd(self.node.id, 'cmd.run', ['rm -f {}'.format(self.node.ldapPassFn)])


    def add_ldap_schema(self):
        try:
            for schemaFile in self.node.schemaFiles:
                saltlocal.cmd(self.node.id, 'cp.get_file', [schemaFile, self.schemaFolder])
        except:
            #self.logIt("Error adding schema")

    def setup_opendj(self):
        self.add_ldap_schema()
        # Copy opendj-setup.properties so user ldap can find it in /opt/opendj
        setupPropsFN = os.path.join(self.node.ldapBaseFolder, 'opendj-setup.properties')
        saltlocal.cmd(self.node.id, 'cp.get_file', [self.node.opendj_setup_properties_file_path, setupPropsFN])
        #change_ownership
        saltlocal.cmd(self.node.id, 'cmd.run', ['chown -R ldap:ldap {}'.format(self.node.ldapBaseFolder)])
        try:
            setupCmd = " ".join([self.node.ldapSetupCommand,
                                      '--no-prompt',
                                      '--cli',
                                      '--propertiesFilePath',
                                      setupPropsFN,
                                      '--acceptLicense'])
            saltlocal.cmd(self.node.id, 'cmd.run', ['su ldap -c {}'.format(setupCmd)])
        except:
            # log "Error running LDAP setup script"

        try:
            saltlocal.cmd(self.node.id, 'cmd.run', ['su ldap -c {}'.format(self.node.ldapDsJavaPropCommand)])
        except:
            #log "Error running dsjavaproperties"


    def configure_opendj(self):
        try:
            config_changes = [['set-global-configuration-prop', '--set', 'single-structural-objectclass-behavior:accept'],
                              ['set-attribute-syntax-prop', '--syntax-name', '"Directory String"',   '--set', 'allow-zero-length-values:true'],
                              ['set-password-policy-prop', '--policy-name', '"Default Password Policy"', '--set', 'allow-pre-encoded-passwords:true'],
                              ['set-log-publisher-prop', '--publisher-name', '"File-Based Audit Logger"', '--set', 'enabled:true'],
                              ['create-backend', '--backend-name', 'site', '--set', 'base-dn:o=site', '--type local-db', '--set', 'enabled:true']]
            for changes in config_changes:
                dsconfigCmd = " ".join([self.node.ldapDsconfigCommand,
                                        '--trustAll',
                                        '--no-prompt',
                                        '--hostname',
                                        self.node.ldap_hostname,
                                        '--port',
                                        self.node.ldap_admin_port,
                                        '--bindDN',
                                        '"%s"' % self.node.ldap_binddn,
                                        '--bindPasswordFile',
                                        self.node.ldapPassFn] + changes)
                saltlocal.cmd(self.node.id, 'cmd.run', ['su ldap -c {}'.format(dsconfigCmd)])
        except:
            #log "Error executing config changes"


    def index_opendj(self):
        try:
            # This json file contains a mapping of the required indexes.
            # [ { "attribute": "inum", "type": "string", "index": ["equality"] }, ...}
            try:
                with open(self.node.indexJson, 'r') as fp:
                    index_json = json.load(fp)
            except:
                #log "bad jason file"
    
            if index_json:
                for attrDict in index_json:
                    attr_name = attrDict['attribute']
                    index_types = attrDict['index']
                    for index_type in index_types:
                        # log "Creating %s index for attribute %s" % (index_type, attr_name)
                        indexCmd = " ".join([self.node.ldapDsconfigCommand,
                                             'create-local-db-index',
                                             '--backend-name',
                                             'userRoot',
                                             '--type',
                                             'generic',
                                             '--index-name',
                                             attr_name,
                                             '--set',
                                             'index-type:%s' % index_type,
                                             '--set',
                                             'index-entry-limit:4000',
                                             '--hostName',
                                             self.node.ldap_hostname,
                                             '--port',
                                             self.node.ldap_admin_port,
                                             '--bindDN',
                                             '"%s"' % self.node.ldap_binddn,
                                             '-j', self.node.ldapPassFn,
                                             '--trustAll',
                                             '--noPropertiesFile',
                                             '--no-prompt'])
                        saltlocal.cmd(self.node.id, 'cmd.run', ['su ldap -c {}'.format(indexCmd)])
            else:
                # log 'NO indexes found %s' % self.node.indexJson
        except:
            #log "Error occured during LDAP indexing"


    def import_ldif(self):
        ldifFolder = '%s/ldif' % self.node.ldapBaseFolder
        for ldif_file_fn in self.node.ldif_files:
            saltlocal.cmd(self.node.id, 'cp.get_file', [ldif_file_fn, ldifFolder])
            ldif_file_fullpath = "%s/ldif/%s" % (self.node.ldapBaseFolder,
                                                 os.path.split(ldif_file_fn)[-1])
            saltlocal.cmd(self.node.id, 'cmd.run', ['chown ldap:ldap {}'.format(ldif_file_fullpath)])
            importCmd = " ".join([self.node.importLdifCommand,
                                  '--ldifFile',
                                  ldif_file_fullpath,
                                  '--backendID',
                                  'userRoot',
                                  '--hostname',
                                  self.node.ldap_hostname,
                                  '--port',
                                  self.node.ldap_admin_port,
                                  '--bindDN',
                                  '"%s"' % self.node.ldap_binddn,
                                  '-j',
                                  self.node.ldapPassFn,
                                  '--append',
                                  '--trustAll'])
            saltlocal.cmd(self.node.id, 'cmd.run', ['su ldap -c {}'.format(importCmd)])

        saltlocal.cmd(self.node.id, 'cp.get_file', ['{}/static/cache-refresh/o_site.ldif'.format(self.node.install_dir), ldifFolder])
        site_ldif_fn = "%s/o_site.ldif" % ldifFolder
        saltlocal.cmd(self.node.id, 'cmd.run', ['chown ldap:ldap {}'.format(site_ldif_fn)])
        importCmd = " ".join([self.node.importLdifCommand,
                              '--ldifFile',
                              site_ldif_fn,
                              '--backendID',
                              'site',
                              '--hostname',
                              self.node.ldap_hostname,
                              '--port',
                              self.node.ldap_admin_port,
                              '--bindDN',
                              '"%s"' % self.node.ldap_binddn,
                              '-j',
                              self.node.ldapPassFn,
                              '--append',
                              '--trustAll'])
        saltlocal.cmd(self.node.id, 'cmd.run', ['su ldap -c {}'.format(importCmd)])

    #TODO : need to deside how to port this function
    def export_opendj_public_cert(self):
        # Load password to acces OpenDJ truststore
        openDjPinFn = '%s/config/keystore.pin' % self.node.ldapBaseFolder
        openDjTruststoreFn = '%s/config/truststore' % self.node.ldapBaseFolder

        openDjPin = None
        try:
            f = open(openDjPinFn)
            openDjPin = f.read().splitlines()[0]
            f.close()
        except:
            #log "Error reding OpenDJ truststore"

        # Export public OpenDJ certificate
        self.run([self.node.keytoolCommand,
                  '-exportcert',
                  '-keystore',
                  openDjTruststoreFn,
                  '-storepass',
                  openDjPin,
                  '-file',
                  self.node.openDjCertFn,
                  '-alias',
                  'server-cert',
                  '-rfc'])

        # Import OpenDJ certificate into java truststore
        self.logIt("Import OpenDJ certificate")

        self.run(["/usr/bin/keytool", "-import", "-trustcacerts", "-alias", "%s_opendj" % self.hostname, \
                  "-file", self.openDjCertFn, "-keystore", self.defaultTrustStoreFN, \
                  "-storepass", "changeit", "-noprompt"])

    def setup(self):
        writeLdapPW()
        setup_opendj()
        configure_opendj()
        index_opendj()
        import_ldif()
        deleteLdapPw()
        export_opendj_public_cert()
