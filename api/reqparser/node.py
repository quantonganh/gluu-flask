from flask.ext.restful import reqparse

# Request parser for node POST and PUT requests
node_reqparser = reqparse.RequestParser()
node_reqparser.add_argument("cluster", type=str, location="form",
                            required=True,
                            help="Cluster ID to which this node will be added")
node_reqparser.add_argument("node_type", type=str, location="form",
                            required=True,
                            help="ldap | oxauth | oxtrust")
