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

test: .clean delete
	@SERVER="$(SALT_MASTER_IPADDR):8080" cram tests

echo:
	@echo $(SALT_MASTER_IPADDR)

.clean:
	@rm -rf tests/*.err

delete: .clean
	@SERVER="$(SALT_MASTER_IPADDR):8080" cram delete

create-ldap-node: .clean delete
	@SERVER="$(SALT_MASTER_IPADDR):8080" cram create-ldap-node

create-oxauth-node: .clean delete
	@SERVER="$(SALT_MASTER_IPADDR):8080" cram create-oxauth-node

.PHONY: delete create-ldap-node
