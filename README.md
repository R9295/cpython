## This is Python version 3.11.0

#### A rough and humble attempt at introducing import policies in Python 3.11.0. Feedback welcome!

### Please see [Demo](#Demo) and [Note](#Notes)

### Introduction
With software supply chain attacks becoming increasingly prevelant and Python lacking a permission system such as the one deno [implements](https://deno.land/manual/getting_started/permissions), third party modules are increasingly becoming uncomfortable to use. Efforts like [packj](https://packj.dev/), [panoptisch](https://github.com/R9295/panoptisch)(written by me), and [semgrep](https://github.com/returntocorp/semgrep) may help alleviate some concerns but static analysis can never satisfy all concerns. Thus, efforts to limit access to sensitive APIs such as network, filesystem and shell, ffi are critical.

### What is this?
This is an experiment to restrict access to modules by modifying the CPython import mechanism.  
If a ``policy.json`` file is present, the interpreter uses the defined policy.  
The structure is as follows:
```
{
  "module": ["everyone", "who", "can", "import", "this", "module"]
}
```
The policy works recursively so you only need to grant permissions to top level dependencies in your project.  
For example, let's say I'm using ``requests`` in my project.
I can grant it ``socket`` access like the following:
```
{
  "socket": ["requests"]
}
```
Now, it wouldn't matter if requests does not *directly* import ``socket``. If any of the sub-dependencies of ``requests`` imports ``socket``, it would allow (or prevent) them.

### Note
**Please note** I am neither a CPython developer nor a C developer. This is a very humble attempt that I would gladly pursue if it is deemed feasible and if anyone is interested!
I'm fairly certain that something such as this [method](https://daddycocoaman.dev/posts/bypassing-python38-audit-hooks-part-1/) can bypass this functionality. 

### Further Work
1. Restrict ``builtins`` such as ``open()`` ``print()`` etc.

### How to use
```
git clone https://github.com/R9295/cpython
cd cpython
git checkout policy
./configure
make -j$(nproc)
./python -m venv venv
source venv/bin/activate
vim /path/to/my/python/file/policy.json
python /path/to/my/python/file
```
### Demo
[![asciicast](https://asciinema.org/a/562388.svg)](https://asciinema.org/a/562388)
