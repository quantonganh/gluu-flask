IP=`hostname -I | cut -d ' ' -f 1`
run:
	@SALT_MASTER_IPADDR=${IP} ./run.py
