IMG:=workspace-new

all: base-build base-run python-build python-run

base-build:
	docker build --platform linux/amd64 -f base.Dockerfile -t $(IMG)-base .

base-run:
	docker run --platform linux/amd64 --privileged -e QEMU_STRACE=1 -d --name $(IMG)-base $(IMG)-base sleep 999

base-exec:
	docker exec -it $(IMG)-base bash

python-build:
	docker build --platform linux/amd64 -f python.Dockerfile -t $(IMG)-python .

python-run:
	docker run --platform linux/amd64 --privileged -d --name $(IMG)-python $(IMG)-python sleep 999

python-exec:
	docker exec -it $(IMG)-python bash

clean:
	docker rm -f $(IMG)-base
	docker rm -f $(IMG)-python
