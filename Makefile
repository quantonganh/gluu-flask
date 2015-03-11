IP=`hostname -I | cut -d ' ' -f 1`
run:
	@SALT_MASTER_IPADDR=${IP} ./run.py

test:
	@py.test tests --cov api --cov-report term-missing
