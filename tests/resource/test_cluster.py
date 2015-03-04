import json


def test_cluster_post(app, db):
    from api.model import GluuCluster

    resp = app.test_client().post(
        "/cluster",
        data={
            "name": "test-cluster-1",
            "description": "test cluster",
            "hostname_ldap_cluster": "cluster-ldap-1",
            "hostname_oxauth_cluster": "cluster-oxauth-1",
            "hostname_oxtrust_cluster": "cluster-oxtrust-1",
            "orgName": "Gluu Federation",
            "orgShortName": "Gluu",
            "countryCode": "US",
            "city": "Austin",
            "state": "Texas",
            "admin_email": "john@example.com",
            "ldaps_port": "1363",
        },
    )
    actual_data = json.loads(resp.data)

    assert resp.status_code == 201
    for field in GluuCluster.resource_fields.keys():
        assert field in actual_data


def test_cluster_get(app, config, cluster, db):
    db.persist(cluster, "clusters")
    resp = app.test_client().get("/cluster/{}".format(cluster.id))
    actual_data = json.loads(resp.data)

    assert resp.status_code == 200
    assert cluster.as_dict() == actual_data
    for field in cluster.resource_fields.keys():
        assert field in actual_data


def test_cluster_get_invalid_id(app):
    resp = app.test_client().get("/cluster/random-invalid-id")
    actual_data = json.loads(resp.data)
    assert resp.status_code == 404
    assert actual_data["code"] == 404
    assert "message" in actual_data


def test_cluster_get_list(app, db, cluster):
    db.persist(cluster, "clusters")
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


def test_cluster_delete(app, db, cluster):
    db.persist(cluster, "clusters")
    resp = app.test_client().delete("/cluster/{}".format(cluster.id))
    assert resp.status_code == 204


def test_cluster_delete_failed(app):
    resp = app.test_client().delete("/cluster/random-invalid-id")
    assert resp.status_code == 404


def test_cluster_update(app, db, cluster):
    db.persist(cluster, "clusters")

    resp = app.test_client().put(
        "/cluster/{}".format(cluster.id),
        data={
            "name": "test-cluster-1",
            "description": "test cluster",
            "hostname_ldap_cluster": "cluster-ldap-1",
            "hostname_oxauth_cluster": "cluster-oxauth-1",
            "hostname_oxtrust_cluster": "cluster-oxtrust-1",
            "orgName": "Gluu Federation",
            "orgShortName": "Gluu",
            "countryCode": "US",
            "city": "Austin",
            "state": "Texas",
            "admin_email": "john@example.com",
            "ldaps_port": "1363",
        },
    )
    actual_data = json.loads(resp.data)
    updated_cluster = db.get(cluster.id, "clusters")

    assert resp.status_code == 200
    assert actual_data == updated_cluster.as_dict()


def test_cluster_update_cluster_not_found(app):
    resp = app.test_client().put("/cluster/random-cluster-id")
    assert resp.status_code == 404
