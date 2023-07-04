## This is Python version 3.13.0 alpha0

#### A rough and humble attempt at sandboxing in Python. Feedback welcome!


### Introduction
With software supply chain attacks becoming increasingly prevelant and Python lacking a permission system such as the one deno [implements](https://deno.land/manual/getting_started/permissions), third party modules are increasingly becoming uncomfortable to use. Efforts like [packj](https://packj.dev/), [panoptisch](https://github.com/R9295/panoptisch)(written by me), and [semgrep](https://github.com/returntocorp/semgrep) may help alleviate some concerns but static analysis is insufficient for dynamic, interpreted languages. Efforts to limit **runtime** access to sensitive APIs such as network, filesystem and shell, ffi are critical.

### What is this?
This is a Proof of Concept sandbox to restrict access to ``socket.connect``. Most supply chain attacks use network or filesystem access to conduct malicious activity. Restricting network access is essential. In order to use ``socket.connect``, you must explicitly declare the URL or IP.


For example:
``` python
permit 'example.com':
    # ok
    foo = socket.socket()
    foo.connect(('example.com', 80))
    # error
    bar = socket.socket()
    bar.connect(('google.com', 80))

# error
bar = socket.socket()
bar.connect(('example.com', 80))
```
Permissions, scoped, stacked and traverse down dependecy trees as they are executed in a context. See: [permit.py](/permit.py) for a detailed example.
The plan is to extend this to filesystem, shell, ffi and env with a friendlier syntax and API

### Known Issues
1. Your dependencies will also be able to call ``permit``. A potential solution could be a global allowlist, but better ideas are in the making. Open to suggestions.
2. If you're using a thirdparty library such as ``requests``. ``socket.connect`` gets an ip address instead of a URL, making filtering painstaking as the address resolution is not deterministic.
This will be fixed as development continues
4. FFI can write to memory in the python address space, so it can probably bypass this.
5. Pip currently does not work as network access is prevented.

### Try it
```
git clone https://github.com/R9295/cpython
cd cpython
./configure
make -j$(nproc)
./python -m venv venv
source venv/bin/activate
# play around with permit.py
(venv) python permit.py
```

### Note
**Please note** I am neither a CPython developer nor a C developer. This solution is not foolproof!
I'm fairly certain that something such as this [method](https://daddycocoaman.dev/posts/bypassing-python38-audit-hooks-part-1/) can bypass this functionality.

