import json
import os


def test_cluster_post(app, config):
    from api.model import GluuCluster

    resp = app.test_client().post("/cluster")
    actual_data = json.loads(resp.data)

    assert resp.status_code == 201
    for field in GluuCluster.resource_fields.keys():
        assert field in actual_data

    # remove test file
    os.unlink("{}/cluster_{}.json".format(config.DB, actual_data["id"]))


def test_cluster_get(app, config, cluster):
    resp = app.test_client().get("/cluster/{}".format(cluster.id))
    actual_data = json.loads(resp.data)

    assert resp.status_code == 200
    assert cluster.as_dict() == actual_data
    for field in cluster.resource_fields.keys():
        assert field in actual_data


def test_cluster_get_invalid_id(app, config):
    resp = app.test_client().get("/cluster/random-invalid-id")
    actual_data = json.loads(resp.data)
    assert resp.status_code == 404
    assert actual_data["code"] == 404
    assert "message" in actual_data


def test_cluster_get_list(app, cluster):
    resp = app.test_client().get("/cluster")
    actual_data = json.loads(resp.data)

    assert resp.status_code == 200
    assert len(actual_data) == 1

    fields = cluster.resource_fields.keys()
    for item in actual_data:
        for field in fields:
            assert field in item


def test_cluster_get_list_empty(app):
    resp = app.test_client().get("/cluster")
    actual_data = json.loads(resp.data)

    assert resp.status_code == 200
    assert len(actual_data) == 0
    assert actual_data == []


def test_cluster_delete(app, cluster):
    resp = app.test_client().delete("/cluster/{}".format(cluster.id))
    actual_data = json.loads(resp.data)

    assert resp.status_code == 200
    assert actual_data["code"] == 200
    assert actual_data["message"] == "Cluster deleted"


def test_cluster_delete_failed(app):
    resp = app.test_client().delete("/cluster/random-invalid-id")
    actual_data = json.loads(resp.data)

    assert resp.status_code == 404
    assert actual_data["code"] == 404
