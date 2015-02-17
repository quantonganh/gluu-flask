import os
from collections import namedtuple

import jsonpickle
import pytest

# Acts as a fake Node until we have a stable Node model
_DummyNode = namedtuple("DummyNode", ["id", "type"])


def test_cluster_persist(config, cluster):
    fp = os.path.join(config.DB, "cluster_{}.json".format(cluster.id))

    # ensure file is created
    assert os.path.exists(fp)

    # ensure we save the data
    with open(fp) as file_:
        expected_data = jsonpickle.decode(file_.read())
        assert cluster.as_dict() == expected_data.as_dict()


@pytest.mark.parametrize("node", [
    _DummyNode(id="1", type="ldap"),
    _DummyNode(id="2", type="oxauth"),
    _DummyNode(id="3", type="oxtrust"),
])
def test_cluster_add_node(cluster, node):
    retval = cluster.add_node(node)

    # ensure node is returned as return value
    assert retval == node

    # ensure node added to cluster
    assert cluster.ldap_nodes[node.id] == node


def test_cluster_add_unsupported_node(cluster):
    with pytest.raises(ValueError):
        node = _DummyNode(id="123", type="random")
        cluster.add_node(node)

        # ensure unsupported node isn't added to cluster
        assert cluster.ldap_nodes == {}
