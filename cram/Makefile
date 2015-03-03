#ifndef SALT_MASTER_IPADDR
#$(error Please set SALT_MASTER_IPADDR)
#endif

usage:
	@echo "Usage:"
	@echo "'make get' to install the dependencies (apt-get & pip)"
	@echo "'make test' to test gluu-flask"

get:
	sudo apt-get install python-pip curl jq
	sudo pip install cram

test:
	@SERVER="localhost:8080" cram tests

test2:
	@SERVER="localhost:8080" cram tests-failing

echo:
	@echo $(SALT_MASTER_IPADDR)

clean:
	@rm -rf tests/*.err
	@rm -rf tests-failing/*.err
