ifndef SALT_MASTER_IPADDR
$(error Please export SALT_MASTER_IPADDR)
endif

usage:
	@echo "Usage:"
	@echo "'make get' to install the dependencies (apt-get & pip)"
	@echo "'make test' to test gluu-flask"

get:
	sudo apt-get install python-pip curl jq
	sudo pip install cram

test:
	@SERVER="$(SALT_MASTER_IPADDR):8080" cram tests

echo:
	@echo $(SALT_MASTER_IPADDR)

clean:
	@rm -rf tests/*.err
