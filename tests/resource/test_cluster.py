def test_cluster_post(app):
    resp = app.test_client().post("/cluster")
    assert resp.status_code == 200
    assert "echo" in resp.data


def test_cluster_get(app, config):
    import json
    import uuid
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    data = cluster.persist(config.DB)

    resp = app.test_client().get("/cluster/{}".format(data["id"]))
    assert resp.status_code == 200
    assert data == json.loads(resp.data)


def test_cluster_delete(app, config):
    import json
    import uuid
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    data = cluster.persist(config.DB)

    resp = app.test_client().delete("/cluster/{}".format(data["id"]))
    assert resp.status_code == 200
    assert json.loads(resp.data)["echo"] == "cluster deleted"
