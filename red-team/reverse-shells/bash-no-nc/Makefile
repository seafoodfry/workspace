NETWORK:=reverse-shells
IMG:=machine

ATTACKER_NAME:=attacker
ATTACKER_CMD:=bash

EXPLOIT_NAME:=exploit
EXPLOIT_CMD:=sleep 999

all: network run

network:
	@echo " > create container network..."
	docker network create $(NETWORK)

build:
	docker build -f Dockerfile -t $(IMG) .

run: build
	@echo " > create exploit container..."
	docker run -d --network $(NETWORK) --name $(EXPLOIT_NAME) ubuntu:20.04 $(EXPLOIT_CMD)
	@echo " > create attacker container..."
	docker run -it --network $(NETWORK) --name $(ATTACKER_NAME) $(IMG) $(ATTACKER_CMD)

ips:
	@echo " > exploit container IP:"
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(EXPLOIT_NAME)
	@echo " > attacker container IP:"
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(ATTACKER_NAME)

exploit-exec: ips
	docker exec -it $(EXPLOIT_NAME) bash

clean:
	@echo " > delete exploit container..."
	docker rm -f $(EXPLOIT_NAME)
	@echo " > delete attacker container..."
	docker rm -f $(ATTACKER_NAME)
	@echo " > delete container network..."
	docker network rm $(NETWORK)
	docker ps
