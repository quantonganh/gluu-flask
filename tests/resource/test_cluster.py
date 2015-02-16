import json
import uuid


def test_cluster_post(app):
    resp = app.test_client().post("/cluster")
    assert resp.status_code == 200
    assert "echo" in resp.data


def test_cluster_get(app, config):
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    data = cluster.persist(config.DB)

    resp = app.test_client().get("/cluster/{}".format(data["id"]))
    actual_data = json.loads(resp.data)

    assert resp.status_code == 200
    assert data == actual_data

    # ensure all resource fields are rendered
    for field in cluster.resource_fields.keys():
        assert field in actual_data


def test_cluster_delete(app, config):
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    data = cluster.persist(config.DB)

    resp = app.test_client().delete("/cluster/{}".format(data["id"]))
    assert resp.status_code == 200
    assert json.loads(resp.data)["echo"] == "cluster deleted"
