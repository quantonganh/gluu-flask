from collections import namedtuple
import pytest

# Acts as a fake Node until we have a stable Node model
_DummyNode = namedtuple("DummyNode", ["id", "type"])


@pytest.mark.parametrize("node", [
    _DummyNode(id="1", type="ldap"),
    _DummyNode(id="2", type="oxauth"),
    _DummyNode(id="3", type="oxtrust"),
])
def test_cluster_add_node(node):
    from api.model import GluuCluster

    cluster = GluuCluster()
    retval = cluster.add_node(node)

    # ensure node is returned as return value
    assert retval == node

    # ensure node added to cluster
    assert cluster.ldap_nodes[node.id] == node


def test_cluster_add_unsupported_node():
    from api.model import GluuCluster

    cluster = GluuCluster()
    with pytest.raises(ValueError):
        node = _DummyNode(id="123", type="random")
        cluster.add_node(node)

        # ensure unsupported node isn't added to cluster
        assert cluster.ldap_nodes == {}


def test_cluster_as_dict():
    from api.model import GluuCluster

    cluster = GluuCluster()
    actual = cluster.as_dict()

    for field in cluster.resource_fields.keys():
        assert field in actual
