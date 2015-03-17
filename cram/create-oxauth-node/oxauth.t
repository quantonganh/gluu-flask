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

  $ PAR2="cluster=$ID&node_type=oxauth&"

  $ echo $PAR2 | post $SERVER/node -i | head -n 1
  HTTP/1.0 202 ACCEPTED
