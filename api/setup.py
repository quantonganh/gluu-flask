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
    def __init__(self):
        self.saltlocal = salt.client.LocalClient()
        #saltlocal.cmd(self.id, 'cmd.run', [dsconfigCmd])
        #saltlocal.cmd(self.id, 'cp.get_file', [schemaFile, self.schemaFolder])

        
    def writeLdapPW(self):
        try:
            f = open(self.ldapPassFn, 'w')
            f.write(self.ldapPass)
            f.close()
            self.run(["/bin/chown", 'ldap:ldap', self.ldapPassFn])
        except:
            self.logIt("Error writing temporary LDAP password.")


    def setup_opendj(self):
        self.logIt("Running OpenDJ Setup")
        try:
            self.add_ldap_schema()
        except:
            self.logIt('Error adding ldap schema', True)
            self.logIt(traceback.format_exc(), True)

        # Copy opendj-setup.properties so user ldap can find it in /opt/opendj
        setupPropsFN = os.path.join(self.ldapBaseFolder, 'opendj-setup.properties')
        shutil.copy("%s/opendj-setup.properties" % self.outputFolder, setupPropsFN)
        self.change_ownership()
        try:
            setupCmd = "cd /opt/opendj ; " + " ".join([self.ldapSetupCommand,
                                      '--no-prompt',
                                      '--cli',
                                      '--propertiesFilePath',
                                      setupPropsFN,
                                      '--acceptLicense'])
            self.run(['/bin/su',
                      'ldap',
                      '-c',
                      setupCmd])
        except:
            self.logIt("Error running LDAP setup script", True)
            self.logIt(traceback.format_exc(), True)

        try:
            dsjavaCmd = "cd /opt/opendj/bin ; %s" % self.ldapDsJavaPropCommand
            self.run(['/bin/su',
                      'ldap',
                      '-c',
                      dsjavaCmd
            ])
        except:
            self.logIt("Error running dsjavaproperties", True)
            self.logIt(traceback.format_exc(), True)


    def configure_opendj(self):
        try:
            self.logIt("Making LDAP configuration changes")
            config_changes = [['set-global-configuration-prop', '--set', 'single-structural-objectclass-behavior:accept'],
                              ['set-attribute-syntax-prop', '--syntax-name', '"Directory String"',   '--set', 'allow-zero-length-values:true'],
                              ['set-password-policy-prop', '--policy-name', '"Default Password Policy"', '--set', 'allow-pre-encoded-passwords:true'],
                              ['set-log-publisher-prop', '--publisher-name', '"File-Based Audit Logger"', '--set', 'enabled:true'],
                              ['create-backend', '--backend-name', 'site', '--set', 'base-dn:o=site', '--type local-db', '--set', 'enabled:true']]
            for changes in config_changes:
                dsconfigCmd = " ".join(['cd %s/bin ; ' % self.ldapBaseFolder,
                                        self.ldapDsconfigCommand,
                                        '--trustAll',
                                        '--no-prompt',
                                        '--hostname',
                                        self.ldap_hostname,
                                        '--port',
                                        self.ldap_admin_port,
                                        '--bindDN',
                                        '"%s"' % self.ldap_binddn,
                                        '--bindPasswordFile',
                                        self.ldapPassFn] + changes)
                self.run(['/bin/su',
                          'ldap',
                          '-c',
                          dsconfigCmd])
        except:
            self.logIt("Error executing config changes", True)
            self.logIt(traceback.format_exc(), True)


    def index_opendj(self):
        try:
            self.logIt("Running LDAP index creation commands")
            # This json file contains a mapping of the required indexes.
            # [ { "attribute": "inum", "type": "string", "index": ["equality"] }, ...}
            index_json = self.load_json(self.indexJson)
            if index_json:
                for attrDict in index_json:
                    attr_name = attrDict['attribute']
                    index_types = attrDict['index']
                    for index_type in index_types:
                        self.logIt("Creating %s index for attribute %s" % (index_type, attr_name))
                        indexCmd = " ".join(['cd %s/bin ; ' % self.ldapBaseFolder,
                                             self.ldapDsconfigCommand,
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
                                             self.ldap_hostname,
                                             '--port',
                                             self.ldap_admin_port,
                                             '--bindDN',
                                             '"%s"' % self.ldap_binddn,
                                             '-j', self.ldapPassFn,
                                             '--trustAll',
                                             '--noPropertiesFile',
                                             '--no-prompt'])
                        self.run(['/bin/su',
                                  'ldap',
                                  '-c',
                                  indexCmd])
            else:
                self.logIt('NO indexes found %s' % self.indexJson, True)
        except:
            self.logIt("Error occured during LDAP indexing", True)
            self.logIt(traceback.format_exc(), True)


    def import_ldif(self):
        self.logIt("Importing userRoot LDIF data")
        ldifFolder = '%s/ldif' % self.ldapBaseFolder
        for ldif_file_fn in self.ldif_files:
            ldifFolder = '%s/ldif' % self.ldapBaseFolder
            self.copyFile(ldif_file_fn, ldifFolder)
            ldif_file_fullpath = "%s/ldif/%s" % (self.ldapBaseFolder,
                                                 os.path.split(ldif_file_fn)[-1])
            self.run(['/bin/chown', 'ldap:ldap', ldif_file_fullpath])
            importCmd = " ".join(['cd %s/bin ; ' % self.ldapBaseFolder,
                                  self.importLdifCommand,
                                  '--ldifFile',
                                  ldif_file_fullpath,
                                  '--backendID',
                                  'userRoot',
                                  '--hostname',
                                  self.ldap_hostname,
                                  '--port',
                                  self.ldap_admin_port,
                                  '--bindDN',
                                  '"%s"' % self.ldap_binddn,
                                  '-j',
                                  self.ldapPassFn,
                                  '--append',
                                  '--trustAll'])
            self.run(['/bin/su',
                      'ldap',
                      '-c',
                      '%s' % importCmd])

        self.logIt("Importing site LDIF")
        self.copyFile("%s/static/cache-refresh/o_site.ldif" % self.install_dir, ldifFolder)
        site_ldif_fn = "%s/o_site.ldif" % ldifFolder
        self.run(['/bin/chown', 'ldap:ldap', site_ldif_fn])
        importCmd = " ".join(['cd %s/bin ; ' % self.ldapBaseFolder,
                              self.importLdifCommand,
                              '--ldifFile',
                              site_ldif_fn,
                              '--backendID',
                              'site',
                              '--hostname',
                              self.ldap_hostname,
                              '--port',
                              self.ldap_admin_port,
                              '--bindDN',
                              '"%s"' % self.ldap_binddn,
                              '-j',
                              self.ldapPassFn,
                              '--append',
                              '--trustAll'])
        self.run(['/bin/su',
                  'ldap',
                  '-c',
                  '%s' % importCmd])


    def deleteLdapPw(self):
        try:
            os.remove(self.ldapPassFn)
            os.remove(os.path.join(self.ldapBaseFolder, 'opendj-setup.properties'))
        except:
            self.logIt("Error deleting ldap pw. Make sure %s is deleted" % self.ldapPassFn)
            self.logIt(traceback.format_exc(), True)


    def export_opendj_public_cert(self):
        # Load password to acces OpenDJ truststore
        self.logIt("Reding OpenDJ truststore")

        openDjPinFn = '%s/config/keystore.pin' % self.ldapBaseFolder
        openDjTruststoreFn = '%s/config/truststore' % self.ldapBaseFolder

        openDjPin = None
        try:
            f = open(openDjPinFn)
            openDjPin = f.read().splitlines()[0]
            f.close()
        except:
            self.logIt("Error reding OpenDJ truststore", True)
            self.logIt(traceback.format_exc(), True)

        # Export public OpenDJ certificate
        self.logIt("Exporting OpenDJ certificate")
        self.run([self.keytoolCommand,
                  '-exportcert',
                  '-keystore',
                  openDjTruststoreFn,
                  '-storepass',
                  openDjPin,
                  '-file',
                  self.openDjCertFn,
                  '-alias',
                  'server-cert',
                  '-rfc'])

        # Import OpenDJ certificate into java truststore
        self.logIt("Import OpenDJ certificate")

        self.run(["/usr/bin/keytool", "-import", "-trustcacerts", "-alias", "%s_opendj" % self.hostname, \
                  "-file", self.openDjCertFn, "-keystore", self.defaultTrustStoreFN, \
                  "-storepass", "changeit", "-noprompt"])

    def setup(self, node):
        writeLdapPW()
        setup_opendj()
        configure_opendj()
        index_opendj()
        import_ldif()
        deleteLdapPw()
        export_opendj_public_cert()

class nodeSetup(object):
    def __init__(self, node = None):
        self.d = {
            'gluuopendj' : ldapSetup,
            #'gluuoxauth' : oxauthSetup,
            #'gluuoxtrust' : oxtrustSetup,
        }
        if node:
            self.node = node
            self.so = d[node.type]()

    def setup(self):
        self.so.setup(self.node)