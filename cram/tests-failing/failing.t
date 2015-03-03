https://bitheap.org/cram/

Return to the working directory
  $ cd $TESTDIR/..

Common aliases
  $ alias get='curl -s'
  $ alias put='curl -s -X PUT --data-binary @-'
  $ alias post='curl -s -X POST --data-binary @-'
  $ alias delete='curl -s -X DELETE'

Currently fails
  $ delete $SERVER/cluster/random-invalid-id -i | head -n 1
  HTTP/1.0 404 NOT FOUND
