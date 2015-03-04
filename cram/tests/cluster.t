https://bitheap.org/cram/

Return to the working directory
  $ cd $TESTDIR/..

Common aliases
  $ alias get='curl -s'
  $ alias put='curl -s -X PUT --data-binary @-'
  $ alias post='curl -s -X POST --data-binary @-'
  $ alias delete='curl -s -X DELETE'

Post invalid data
  $ echo "invalid" | post $SERVER/cluster | jq -r .message
  Missing required parameter name in the post body

  $ echo "invalid" | post $SERVER/cluster -i | head -n 1
  HTTP/1.0 400 BAD REQUEST

Get invalid data
  $ get $SERVER/cluster/random-invalid-id -i | head -n 1
  HTTP/1.0 404 NOT FOUND

  $ get $SERVER/cluster/random-invalid-id | jq -r .code
  404

  $ get $SERVER/cluster/random-invalid-id | jq -r .message
  Cluster not found

Create POST parameter string from params.txt
  $ PAR=`cat params.txt | tr '\n' '&'`

Create a cluster and try getting it by ID, check if responses are identical
  $ OUT1=`echo $PAR | post $SERVER/cluster`
  $ ID1=`echo $OUT1 | jq -r .id`
  $ OUT2=`get $SERVER/cluster/$ID1`
  $ test "$OUT1" = "$OUT2" && echo true
  true

  $ JSON=`get $SERVER/cluster/$ID1`

  $ echo $JSON | jq -r .name
  test-cluster-1

  $ echo $JSON | jq -r .description
  test cluster

  $ delete $SERVER/cluster/$ID1 -i | head -n 1
  HTTP/1.0 204 NO CONTENT

Create some clusters
  $ for i in 1 2 3 4 5
  > do
  >   echo $PAR | post $SERVER/cluster > /dev/null
  > done

Delete all clusters
  $ CLUSTERS=`get $SERVER/cluster | jq -a -r '.[] | .id'`
  $ for i in $CLUSTERS
  > do
  >   delete $SERVER/cluster/$i
  > done

There should be no clusters left
  $ get $SERVER/cluster
  []

  $ delete $SERVER/cluster/random-invalid-id -i | head -n 1
  HTTP/1.0 404 NOT FOUND
