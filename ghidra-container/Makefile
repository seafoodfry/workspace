CONTAINER := ghidra
GHIDRA_CONTAINER_PATH := /home/noroot/ghidra
GHIDRA_SERVER := $(GHIDRA_CONTAINER_PATH)/server/ghidraSvr
GHIDRA_CLIENT := $(GHIDRA_CONTAINER_PATH)/support/launch.sh

all: build
	docker run -it $(CONTAINER) bash

server: build
	docker run -it -p 13100:13100 $(CONTAINER) $(GHIDRA_SERVER) console

client: build
	docker run -it --cpus 2 --memory 4g -e DISPLAY="host.docker.internal:0" $(CONTAINER) $(GHIDRA_CLIENT) fg Ghidra 768M "" ghidra.GhidraRun

docs: build
	docker run -p 8080:8080 $(CONTAINER) python3 -m http.server --bind 0.0.0.0 8080

build:
	docker build -t $(CONTAINER) .
