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
import codecs
import os.path
import time

from api.helper.common_helper import run
from api.setup.oxauth_setup import OxAuthSetup


class OxTrustSetup(OxAuthSetup):
    def copy_tomcat_conf(self):
        # copy static template
        remote_dest_dir = os.path.join(self.node.tomcat_conf_dir, "template", "conf")
        self.logger.info("copying {}".format(self.node.oxtrust_cache_refresh_properties))
        self.saltlocal.cmd(self.node.id, "cmd.run", ["mkdir -p {}".format(remote_dest_dir)])
        run("salt-cp {} {} {}".format(
            self.node.id,
            self.node.oxtrust_cache_refresh_properties,
            os.path.join(
                remote_dest_dir,
                os.path.basename(self.node.oxtrust_cache_refresh_properties),
            ),
        ))

        ctx = {
            "inumOrg": self.cluster.inumOrg,
            "inumOrgFN": self.cluster.inumOrgFN,
            "ldaps_port": self.cluster.ldaps_port,
            "hostname": self.node.hostname,
            "inumAppliance": self.cluster.inumAppliance,
            "inumApplianceFN": self.cluster.inumApplianceFN,
            "ldap_binddn": self.node.ldap_binddn,
            "orgName": self.cluster.orgName,
            "orgShortName": self.cluster.orgShortName,
            "admin_email": self.cluster.admin_email,
            "tomcat_log_folder": self.node.tomcat_log_folder,
            "shibJksPass": self.node.shib_jks_pass,
            "shibJksFn": self.node.shib_jks_fn,
            "oxTrustConfigGeneration": self.node.oxtrust_config_generation,
            "oxauth_client_id": self.node.oxauth_client_id,
            "encoded_ox_ldap_pw": self.node.encoded_ox_ldap_pw,
            "encoded_shib_jks_pw": self.node.encoded_shib_jks_pw,
            "oxauthClient_encoded_pw": self.node.oxauth_client_encoded_pw,

            # FIXME: the following keys are left blank
            #        it will be populated eventually
            "ldap_hostname": "",
        }

        # rendered templates
        conf_templates = (
            self.node.oxtrust_properties,
            self.node.oxtrust_ldap_properties,
            self.node.oxtrust_log_rotation_configuration,
            self.node.oxauth_static_conf_json,
        )
        for tmpl in conf_templates:
            rendered_content = ""
            try:
                with codecs.open(tmpl, "r", encoding="utf-8") as fp:
                    rendered_content = fp.read() % ctx
            except Exception as exc:
                self.logger.error(exc)

            file_basename = os.path.basename(tmpl)
            local_dest = os.path.join(self.build_dir, file_basename)
            remote_dest = os.path.join(self.node.tomcat_conf_dir, file_basename)

            try:
                with codecs.open(local_dest, "w", encoding="utf-8") as fp:
                    fp.write(rendered_content)
            except Exception as exc:
                self.logger.error(exc)

            self.logger.info("copying {}".format(local_dest))
            run("salt-cp {} {} {}".format(self.node.id, local_dest,
                                          remote_dest))

    def setup(self):
        start = time.time()
        self.logger.info("oxTrust setup is started")

        # generate oxtrustLdap.properties, oxTrust.properties,
        # oxauth-static-conf.json, oxTrustLogRotationConfiguration.xml
        self.copy_tomcat_conf()

        # Create or copy key material to /etc/certs
        # FIXME: missing /etc/certs/httpd.crt
        self.gen_cert()

        # Configure apache httpd to proxy AJP:8009
        self.copy_httpd_conf()

        # TODO: Configure tomcat to run oxtrust war file

        elapsed = time.time() - start
        self.logger.info("oxTrust setup is finished ({} seconds)".format(elapsed))
        return True
