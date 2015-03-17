https://bitheap.org/cram/

Return to the working directory
  $ cd $TESTDIR/..

Common aliases
  $ alias get='curl -s'
  $ alias put='curl -s -X PUT --data-binary @-'
  $ alias post='curl -s -X POST --data-binary @-'
  $ alias delete='curl -s -X DELETE'

Delete all nodes
  $ NODES=`get $SERVER/node | jq -a -r '.[] | .id'`
  $ for i in $NODES
  > do
  >   delete $SERVER/node/$i
  > done

There should be no nodes left
  $ get $SERVER/node
  []

Delete all clusters
  $ CLUSTERS=`get $SERVER/cluster | jq -a -r '.[] | .id'`
  $ for i in $CLUSTERS
  > do
  >   delete $SERVER/cluster/$i
  > done

There should be no clusters left
  $ get $SERVER/cluster
  []
