from flask.ext.restful import reqparse

# Request parser for cluster POST and PUT requests
cluster_reqparser = reqparse.RequestParser()

cluster_reqparser.add_argument("name", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("description", type=str, location="form",
                               required=True)

cluster_reqparser.add_argument("hostname_ldap_cluster", type=str,
                               location="form", required=True)
cluster_reqparser.add_argument("hostname_oxauth_cluster", type=str,
                               location="form", required=True)
cluster_reqparser.add_argument("hostname_oxtrust_cluster", type=str,
                               location="form", required=True)

cluster_reqparser.add_argument("orgName", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("orgShortName", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("countryCode", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("city", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("state", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("admin_email", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("ldap_replication_admin_pw", type=str,
                               location="form", required=True)
