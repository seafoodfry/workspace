FROM --platform=linux/amd64 gcr.io/oss-fuzz-base/base-builder:v1

RUN apt-get update -y && \
    apt-get install vim strace -y

WORKDIR /app
COPY use-after-free.c .
RUN clang -fsanitize=address -O1 -fno-omit-frame-pointer -g use-after-free.c -o heap-use-after-free
