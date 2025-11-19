# ainakan-python

Python bindings for [Ainakan](https://ainakan.re).

# Some tips during development

To build and test your own wheel, do something along the following lines:

```
set AINAKAN_VERSION=16.0.1-dev.7 # from C:\src\ainakan\build\tmp-windows\ainakan-version.h
set AINAKAN_EXTENSION=C:\src\ainakan\build\ainakan-windows\x64-Release\lib\python3.10\site-packages\_ainakan.pyd
cd C:\src\ainakan\ainakan-python\
pip wheel .
pip uninstall ainakan
pip install ainakan-16.0.1.dev7-cp34-abi3-win_amd64.whl
```
