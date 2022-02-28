# Ghidra

```
wrapper.app.parameter.1=-a0
wrapper.app.parameter.2=${ghidra.repositories.dir}
```

```
wrapper.app.parameter.1=-a0
wrapper.app.parameter.2=-u
wrapper.app.parameter.3=-ip
wrapper.app.parameter.4=0.0.0.0
wrapper.app.parameter.5=${ghidra.repositories.dir}
```

* `-a0` means that a private user password will be used for authentication
* `-u` will enable users to be prompted for user ID
* `-ip 0.0.0.0` is the default but we want to explicitly enable it`

```
brew install --cask xquartz
brew install socat
```

```
Exception in thread "main" java.lang.UnsatisfiedLinkError: /opt/java/openjdk/lib/libawt_xawt.so:
    libXext.so.6: cannot open shared object file: No such file or directory
```

```
Exception in thread "main" java.lang.UnsatisfiedLinkError: /opt/java/openjdk/lib/libawt_xawt.so:
    libXrender.so.1: cannot open shared object file: No such file or directory
```

```
Exception in thread "main" java.lang.UnsatisfiedLinkError: /opt/java/openjdk/lib/libawt_xawt.so:
    libXi.so.6: cannot open shared object file: No such file or directory
```

`libxi6`

https://bitsanddragons.wordpress.com/2020/06/05/address-already-in-use-socat-not-working-on-osx/
