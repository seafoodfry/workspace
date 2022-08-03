# An OS From Scratch: Pt 1

## Overview

In short, we will try and figure out how to develop and OS from scratch.
Why? Because even a little bit of familiarity with system internals/programming will help us.
We will primarily focus on Linux here, becuase it is the OS/Kernel with the most open-sourced documentation and the
one for which most tutorials are written.
Let's use this as a starting point and as a model.

For this, and most other OS-related posts, we will use Qemu (its a widely used tool with descent documentation and an open community).
We will do all of this work on a remote server, which means we will SSH into it.

---

## SSH and the X Server

Let's talk about X11, also called X Windows System, before we get started with SSH.

As wikipedia explains, [X Windows system](https://en.wikipedia.org/wiki/X_Window_System)
> The X server is typically the provider of graphics resources and keyboard/mouse events to X clients, meaning that
> the X server is usually running on the computer in front of a human user, while the X client applications run anywhere
> on the network and communicate with the user's computer to request the rendering of graphics content and receive events from input devices including keyboards and mice.
> ...
> Here, rather than a remote database being the resource for a local app, the user's graphic display and input devices become
> resources made available by the local X server to both local and remotely hosted X client programs who need to share the user's graphics and input devices to communicate with the user.
>
> ...
> The server accepts requests for graphical output (windows) and sends back user input (from keyboard, mouse, or touchscreen).

So your local computer runs an X server, and our server runs an an X111 client.

Turns out that X111 is also mindful of authorization, it can have "trusted" and "untrusted" client.
Wikipedia has some useful context for us
> In the X Window System, programs run as X clients, and as such they connect to the X display server, possibly via a computer network.
> Since the network may be accessible to other users, a method for forbidding access to programs run by users different from the one who is logged in is necessary.
> [X Window authorization](https://en.wikipedia.org/wiki/X_Window_authorization)

The same page mentions that a method of authentication is a cookie-based on in which a "magic cookie" is stored in `~/.Xauthority`.
In this case, there is also a `xauth` application which is used to access the cookie.

From the same wikipedia page
> The SSH utility (when invoked with option -X or option ForwardX11) tunnels X11 traffic from remotely invoked clients to the local server.
> It does so by setting at the remote site the DISPLAY environment variable to point to a local TCP socket opened there by sshd,
> which then tunnels the X11 communication back to ssh. Sshd then also calls xauth to add at the remote site an MIT-MAGIC-COOKIE-1
> string into .Xauthority there, which then authorizes X11 clients there to access the ssh user's local X server.

Untrusted clients will be watched more carefully due to this.
For this untrusted clients, SSH will try and make X111 forwarding safer by not trusting them (ha) and putting additional preventive measures in place.
Whereas a trusted client means that you are sure that no entity in your (ssh) server will try to abuse the X111 forwarding connection to try and get into
your local computer.


**Note:** If you are on a Mac, you'll need to install X Window XQuartz (Apple's version of the X server), see [www.xquartz.org/](https://www.xquartz.org/).
You will very likely need to reboot if you just installed xquartz.

Let's begin SSHing.
If you read the man page for SSH you may have seen these flags
> **-X**
> X11 forwarding should be enabled with caution. Users with the ability to bypass file permissions on the remote host
> (for the user's X authorization database) can access the local X11 display through the forwarded connection.
> An attacker may then be able to perform activities such as keystroke monitoring.
>
> For this reason, X11 forwarding is subjected to X11 SECURITY extension restrictions by default.
> Please refer to the ssh -Y option and the ForwardX11Trusted directive in ssh_config(5) for more information.
>
> **-Y**
> Enables trusted X11 forwarding. Trusted X11 forwardings are not subjected to the X11 SECURITY extension controls.
> [man ssh](https://manpages.debian.org/buster/openssh-client/ssh.1.en.html#Y)


The man pages for ssh recommends we read the man page for sshd_config.
Looking at the [man sshd_config pages](https://manpages.debian.org/buster/openssh-client/ssh_config.5.en.html#ForwardX11)
> **ForwardX11**
>   Specifies whether X11 connections will be automatically redirected over the secure channel and DISPLAY set. The argument must be yes or no (the default).
>
>   X11 forwarding should be enabled with caution. Users with the ability to bypass file permissions on the remote host
>   (for the user's X11 authorization database) can access the local X11 display through the forwarded connection.
>   An attacker may then be able to perform activities such as keystroke monitoring if the ForwardX11Trusted option is also enabled.
>
> **ForwardX11Trusted**
>   If this option is set to yes, (the Debian-specific default), remote X11 clients will have full access to the original X11 display.
>
>   If this option is set to no (the upstream default), remote X11 clients will be considered untrusted and prevented from stealing
>   or tampering with data belonging to trusted X11 clients. Furthermore, the xauth(1) token used for the session will be set to expire after 20 minutes.
>   Remote clients will be refused access after this time.
>
>   See the X11 SECURITY extension specification for full details on the restrictions imposed on untrusted clients.


The reason for taking that brief detour is because if you ssh into your server, and turn on x111 forwarding, you may see this
```
$ ssh -X ubuntu@ip-or-dns

Warning: untrusted X11 forwarding setup failed: xauth key data not generated
...
```

Some answers tell you to use `ssh -Y` but now you now there is a better way!
In Mac, open up xquartz > Preferences > Security and enable _Authenticate connections_.

If that still results in some xauth-related warning, then take a look at the tips (they'll be at the bottom of the page, ignore the accepted answer) in
[What does "Warning: untrusted X11 forwarding setup failed: xauth key data not generated" mean when ssh'ing with -X?](https://serverfault.com/questions/273847/what-does-warning-untrusted-x11-forwarding-setup-failed-xauth-key-data-not-ge).


```
#!/bin/bash
set -x
sudo apt-get update -y
sudo apt-get install qemu-system-x86 -y
sudo apt-get install build-essential cmake lld nasm -y
```

## The Boot Loader

To begin with out setup, let's write a simple boot loader.
This thing will be loaded by a BIOS because we will write a disk sector with a magic number (telling the BIOS to loaded it up).
The magic number is `0xaa55` and a sector is 512 bytes long, or at least that was the convention when 32 bits system were more popular.
The convention is that this amgic number needs to be in the last 2 bytes of the 512 bytes-long sector.

**Words, Bytes, and Hec**
A bit of convention.
A byte has 2^8 possible values.
In hex, this means that we can use two hex digits to represent a byte (2^8 = 256 = 16 * 16 = 2^4 * 2^4).
A lot of confusion will then arrive due to how long a word is, this depends on the computer architecture.
Nowadays, everything is 64-bit, so a word is more commonly 4 bytes (8 hex digits).
In the older days, with 16-bit architectures being common and 32-bit architectures being a huge thing, a word used to be 2 bytes.

### Intel

Using intel assembly syntax (we will use the netwide assembler), we can do the following
```nasm
; An infinite loop to keep the system up.
loop:
    jmp loop

; A bunch of zeros to align the magic number to the end of a 512 byte long sector.
times 510-($-$$) db 0

; Finally, the magic number.
dw 0xaa55
```

To make sense of this example keep in mind that
- Hex numbers go from 0 to 15 so you need a byte for each hex number.
- The magic number is already claiming 2 bytes at the end of the 512 bytes-long secotr (510 bytes remaining).
- A word is 2 bytes long, so `dw` (define word) can take the magic number as input
    - The BIOS runs in 16-bit real mode, this also what computers were using back in the day (16 bits == 2 bytes == 1 word).
- `times` is a utility offered by nasm to mean that the given instruction must be assembled a given ammount of times (`times <number-of-times> <instruction>`).
    - `$` evaluates to the assembly position at the beginning of the line containing the expression.
    - `$$` evaluates to the beginning of the current section.
    - `db` defines a byte

Now assemble and boot it up
```
nasm boot_loader.asm -f bin -o boot_loader.bin
qemu-system-i386 boot_loader.bin
```

You should see a black screen telling you that it booted from the hard disk.

### ATT

Now in ATT syntax and with GAS
```gas
# An infinite loop to keep the system up.
init:
  jmp init

# A bunch of zeros to align the magic number to the end of a 512 byte long sector.
.fill 510-(.-init), 1, 0

# Finally, the magic number.
.word 0xaa55
```

And to but it up
```
as -o boot.o boot.s
ld -o boot.bin --oformat=binary boot.o
qemu-system-i386 boot.bin
```

Bit of explanation on the syntax
- `.fill` is a preprocessor directive available in gas (GNU as) whose arguments are "count, size, value" (size in bytes).

### References

- [Writing an x86 "Hello world" bootloader with assembly](https://50linesofco.de/post/2018-02-28-writing-an-x86-hello-world-bootloader-with-assembly)
- [x86 Assembly Language Programming](https://cs.lmu.edu/~ray/notes/x86assembly/)
- [NASM: Assembly - Basic Syntax](https://www.tutorialspoint.com/assembly_programming/assembly_basic_syntax.htm)
