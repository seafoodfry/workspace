# Fuzzing and Other Issues

[github.com/google/atheris](https://github.com/google/atheris)

```
sudo apt-get install build-essential cmake
```

```
git clone https://github.com/llvm/llvm-project.git --depth 1 -b llvmorg-14.0.5
cd llvm-project
mkdir build
cd build
cmake -DLLVM_ENABLE_PROJECTS='clang;compiler-rt' -G "Unix Makefiles" ../llvm
time make -j 3 2>&1 | tee output.log # This step is very slow
```

If you get a random
```
fatal error: Killed signal terminated program cc1plus
```
Then it may be because you are requesting too many threads, try lowering `make -n <n>` to the number of cores you have (don't know why atheris recommends 100).
And if you get `no space left on device` errors, make sure you have a disk device with plenty of space (at least 64Gi).

```
collect2: fatal error: ld terminated with signal 9 [Killed]
```
System overload or memory exhaustion.
Running on a machine with 4vCPU and 16Gi took 106m17.197s before running into that error.

```
cmake -DLLVM_ENABLE_PROJECTS='clang;compiler-rt' -DLLVM_USE_LINKER=lld -G "Unix Makefiles" ../llvm
```

```
#!/bin/bash
sudo apt update -y
sudo apt-get install build-essential cmake lld -y
git clone https://github.com/llvm/llvm-project.git --depth 1 -b llvmorg-14.0.5 /home/ubuntu/llvm-project
sudo chown -R ubuntu:ubuntu /home/ubuntu/llvm-project
```

* compiling with a t3.2xlarge took more than 2hrs, it failed with the classic ld signal killed. Ran with `make -j 2`, ld as linker, and a gp3 volume of 100G.
* running with lld as linker on a t3.2xlarge, with 200G gp3 volume and `mkae -j 2` did work and it took 178 minutes. It ended up taking 102G of storage.
* running with lld as linker on a t3.2xlarge, with a 128G gp3 volume and `make -j 2` did work and it took 177 minutes. It ended up taking 102G of storage again.
* running with lld as linker on a t3.2xlarge, with a 120G gp3 volume and `make -j 3` did work and it took 120 minutes. It ended up taking 102G of storage again.
* running with lld as linker on a t3a.2xlarge with a 120G gp3 volume and `make -j 3` did work and it took 132 minutes. It ended up taking 120G of storage again.
* running with lld as linker on a t3a.xlarge with a 120G gp3 volume and `make -j 4` did work and it took 178 minutes. It ended up taking 120G of storage again.

Trying to pip install atheris will result on it installing instructions to compile the llvm-projects repo.
This will not work on ARM64, the make process will exit with no clear error message before itgets to 50%.

Next thing we tried was to use the oss-fuzz images published by Google.
These are supposed to have LibFuzzer and the AddressSanitizer, among many other things.

Tried testing the address sanitizer inside of a container and would result in an errno 137 with a `Killed` message.
This is indicative of the Linux memory manager killing it.
Some diggng around we came up with
```
dmesg -T | egrep -i 'killed process'
[Sat Jun 11 22:16:05 2022] Out of memory: Killed process 14615 (heap-use-after-)...
```
Note that for the above to work, the containers need to run with `--privileged`.
So the AddressSanitizer example showing a heap-after-use issue was running fine on a host machine but it'd be killed in
a container by the memory manager.
Another interesting thing to notice is that running `dmesg` in a non-Linux host (e.g., Mac) would result in different output.

Another way we tried to investigate why the process was being killed was by using strace.
When we ran this on a container running on a mac host we saw the following
```
strace ./heap-use-after-free
strace: test_ptrace_get_syscall_info: PTRACE_TRACEME: Function not implemented
strace: ptrace(PTRACE_TRACEME, ...): Function not implemented
strace: PTRACE_SETOPTIONS: Function not implemented
strace: detach: waitpid(51): No child processes
strace: Process 51 detached
```
Turns out that if you open the Activity monitor on a mac and see `qemu-system-aarch64` running, thats from Docker.
And the qemu user space emulator does not implement ptrace.
You can get some "tracing" if you run your container with `-e QEMU_STRACE=1`.
See
[QEMU User space emulator](https://www.qemu.org/docs/master/user/main.html).
