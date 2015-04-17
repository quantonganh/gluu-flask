# Install gluu-flask using SaltStack

## Install Salt minion

```
$ sudo add-apt-repository ppa:saltstack/salt
$ sudo apt-get update
$ sudo apt-get install salt-minion
```

## Download the template

```
mkdir /srv/salt
git init /tmp/gluu-flask
cd /tmp/gluu-flask
git config core.sparseCheckout true
git remote add -f origin git@github.com:quantonganh/gluu-flask.git
echo salt > .git/info/sparse-checkout
git pull origin master
mv salt /srv/salt/gluu-flask
```

## Install gluu-flask

```
salt-call --local state.sls gluu-flask -l debug
```

## Swagger UI

Point the web browser to: http://IP:8080/api/spec.html
Click on Show/Hide to show the API

1. Create a cluster:
  1. Click on `POST /cluster`:
  2. Enter all the required parameters
  3. Click "Try it out!" button
  4. Copy the cluster ID from the Response Body:

  ```
  "id": "313c7b60-1c53-465f-b021-52883540418a",
  ```

2. Create a LDAP node:
  1. Click on `POST /node`
  2. Enter the cluster ID that had been copied
  3. Enter `ldap` for the `node_type`
  4. Click on "Try it out!" button, make sure that the reponse code is 202.
  5. See the progress by checking the log file on the server:

  ```
  less +F /tmp/gluuopendj-build-E57SQh.log
  ```

  When it is done, the log said:

  ```
  - INFO  - LDAP setup is finished (173.617697001 seconds)
  - INFO  - saving to database
  - INFO  - removing temporary build directory /tmp/tmp6EWeKN
  ```

  Back to the Swagger UI, click on the `/GET /cluster{cluster_id}`, enter the
  cluster id, click on "Try it out!", verify that ldap node has been created:

  ```
  "ldap_nodes": [
    "46ad8cb8c62f"
  ],
  "ldaps_port": "1636",
  "name": "example",
  "orgName": "example",
  "orgShortName": "exp",
  ```

3. Create a oxauth, oxtrust node:
  Do the same as ldap node, but just change the `node_type` to the
  corresponding value.
