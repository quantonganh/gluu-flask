https://bitheap.org/cram/

Return to the working directory
  $ cd $TESTDIR/..

Common aliases
  $ alias get='curl -s'
  $ alias put='curl -s -X PUT --data-binary @-'
  $ alias post='curl -s -X POST --data-binary @-'
  $ alias delete='curl -s -X DELETE'

Create POST parameter string from params.txt
  $ PAR=`cat params.txt | tr '\n' '&'`

Create a cluster, save ID
  $ ID=`echo $PAR | post $SERVER/cluster | jq -r .id`

Create a node with invalid data
  $ echo node_type=ldap | post $SERVER/node | jq -r .message
  Cluster ID to which this node will be added

  $ echo cluster=invalid-id | post $SERVER/node | jq -r .message
  ldap | oxauth | oxtrust

Get invalid data
  $ get $SERVER/node/random-invalid-id -i | head -n 1
  HTTP/1.0 404 NOT FOUND

  $ get $SERVER/node/random-invalid-id | jq -r .code
  404

  $ get $SERVER/node/random-invalid-id | jq -r .message
  Node not found
