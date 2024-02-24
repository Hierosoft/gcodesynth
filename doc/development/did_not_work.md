# Did not work

2021-04-04 I e-mailed the PyAudiere author to request he places PyAudiere on GitHub.

See also improved audiogen_p3 documentation at https://github.com/rguisewite/audiogen_p3/pull/1

### audiogen usage
(guesswork based on examples; never got it working)
```Python
# python3 -m pip install https://github.com/rguisewite/audiogen_p3/archive/refs/heads/master.zip
# ^ audiogen_p3
import audiogen_p3 as audiogen
# beats = audiogen.mixer((audiogen.tone(440), audiogen.tone(445)), [(constant(1), constant(1)),])
# ^ fails: "AttributeError: module 'audiogen_p3' has no attribute 'mixer'"

import itertools
import sys
# from audiogen_p3.generators.util import constant
# ^ doesn't work: "ModuleNotFoundError: No module named 'audiogen_p3.generators.util'; 'audiogen_p3.generators' is not a package"
audiogen.sampler.play(audiogen.beep(frequency=840, seconds=0.25))
```

### Getting audiogen install to work
```bash
# optional:
# sudo apt install -y python3-pip-autoremove
# ^ The command for the Python 3 version is `pip3-autoremove`.

# fails due to Python 2 syntax:
# python3 -m pip install audiogen
# pip3-autoremove audiogen

# Guessed since PyAudio has portaudio bindings:
sudo apt install -y libportaudiocpp0 portaudio19-dev
# As per <https://github.com/rguisewite/audiogen_p3>:
# python3 -m pip install audiogen_p3
# ^ found via commit history at [rguisewite's fork](https://github.com/rguisewite/audiogen_p3)
# python3 -m pip install --allow-external PyAudio --allow-unverified PyAudio PyAudio
# ^ fails due to Python 2 syntax
# python3 -m pip install PyAudio
# still says:
# "Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: module 'audiogen_p3' has no attribute 'mixer'"
# So do some guesswork:
# pip3-autoremove PyAudio
sudo apt install -y python3-pyaudio
# ^ installs libportaudio2
# pip3-autoremove audiogen_p3
python3 -m pip install https://github.com/rguisewite/audiogen_p3/archive/refs/heads/master.zip

# See also: another fork with more tests and similar Python 3 fixes: <https://github.com/gdusbabek/audiogen>


# ^ from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# found via <https://stackoverflow.com/questions/54998028/how-do-i-install-pyaudio-on-python-3-7>

```

### Fixing audiogen

```python
>>> import audiogen
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/owner/.local/lib/python3.7/site-packages/audiogen/__init__.py", line 2, in <module>
    from .sampler import frame_rate
  File "/home/owner/.local/lib/python3.7/site-packages/audiogen/sampler.py", line 64
    except IOError, e:
                  ^
SyntaxError: invalid syntax
```
diagnosis: It is using Python 2 syntax.
#### Switch to ([rguisewite's Python 3 fork](https://github.com/rguisewite/audiogen_p3) of audiogen) )
Mixer isn't present, and there isn't a clear way to

#### Switch to https://github.com/gdusbabek/audiogen

```bash
pip3-autoremove audiogen_p3
https://github.com/gdusbabek/audiogen
# python3 -m pip install https://github.com/gdusbabek/audiogen/archive/refs/heads/master.zip
# Only the following branch has the new tests and Python 3 fixes:
python3 -m pip install https://github.com/gdusbabek/audiogen/archive/refs/heads/add_tests.zip
# still has:
# >>> import audiogen
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/home/owner/.local/lib/python3.7/site-packages/audiogen/__init__.py", line 2, in <module>
#     from .sampler import frame_rate
#   File "/home/owner/.local/lib/python3.7/site-packages/audiogen/sampler.py", line 64
#     except IOError, e:
#                   ^
# SyntaxError: invalid syntax
pip3-autoremove audiogen
```

Switch back to the rguisewite fork.

### Fixing the weegreenblobbie fork of nsound (doesn't work yet)
The problem is not swig because though it contains Py_InitModule (not PyInstance_Type), swig (at least >=4.02) checks for Python < 3 before using that (swig3.0 (from Debian 10) uses `Py_InitModule` (and `PyInstance_Type`?) apparently so it may be non-working on Python >= 3.6 (in <https://docs.python.org/3.5/extending/newtypes.html?highlight=pyinstance_type> not 3.6 nor 3.7 docs: <https://docs.python.org/3.7/extending/newtypes.html?highlight=pyinstance_type>))

```bash
sudo apt install -y scons swig libportaudiocpp0 portaudio19-dev
sudo apt remove -y swig
DOWNLOADS=$HOME/Downloads
SWIG_DL_VER="4.0.2"
SWIG_EX_NAME=swig-$SWIG_DL_VER
SWIG_DL_NAME=swig-$SWIG_DL_VER.tar.gz
SWIG_DL_DST=$DOWNLOADS/$SWIG_DL_NAME
SWIG_URL="https://iweb.dl.sourceforge.net/project/swig/swig/swig-$SWIG_DL_VER/$SWIG_DL_NAME"
if [ ! -f "$SWIG_DL_DST" ]; then
    wget -O "$SWIG_DL_DST" "$SWIG_URL"
    if [ $? -ne 0 ]; then
        echo "Error: 'wget -O \"$SWIG_DL_DST\" \"$SWIG_URL\"' failed."
        sleep 1
        exit 1
    fi
fi
cd "$DOWNLOADS"
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"$DOWNLOADS\"' failed."
    sleep 1
    exit 1
fi
if [ ! -d "$SWIG_EX_NAME" ]; then
    tar -xf "$SWIG_DL_NAME"
    if [ $? -ne 0 ]; then
        echo "Error: 'tar -xf \"$SWIG_DL_NAME\"' failed."
        sleep 1
        exit 1
    fi
else
    echo "* using existing $SWIG_EX_NAME"
fi
cd "$SWIG_EX_NAME"
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"$SWIG_EX_NAME\"' failed."
    sleep 1
    exit 1
fi
./configure
make
sudo make install
grep Py_InitModule --line-number -r
# ^ OK (only has Python 3.5 & 2 stuff inside of cases for < 3):
#   /usr/local/share/swig/4.0.2/python/pyinit.swg:470:  m = Py_InitModule(SWIG_name, SwigMethods);
#   /usr/local/share/swig/4.0.2/python/pyrun.swg:1394:  PyObject *module = Py_InitModule("swig_runtime_data" SWIG_RUNTIME_VERSION, swig_empty_runtime_method_table);
#   (same for the git version--searched <https://github.com/swig/swig/commit/18bc3e287b17927584361a2b0ff70a14c64e61b4>)
grep PyInstance_Type --line-number -r
# ^ OK (no results)
#endif

# python2 -m pip install --user nsound
# ^ python2 only
# python3 -m pip install --user https://github.com/weegreenblobbie/nsound/archive/refs/heads/master.zip
# ^      File "/tmp/pip-req-build-7vqdghi2/setup.py", line 190, in process_nsound_h
#          keys.sort()
#      AttributeError: 'dict_keys' object has no attribute 'sort'
# ^ until the following issue is resolved: <https://github.com/weegreenblobbie/nsound/issues/17>
# python3 -m pip install --user ~/git/nsound
python3 -m pip uninstall nsound
python3 -m pip install --user https://github.com/poikilos/nsound/archive/refs/heads/master.zip
```


(starting from <https://github.com/weegreenblobbie/nsound/commit/25bc006298d6d19833e1550cc8a76a8a0a5d034c>;
tested on Debian 10 Buster)

Importing Nsound in Python 3 after fixing setup to work with Python 3 results in:
```
Traceback (most recent call last):
  File "/home/owner/.local/lib/python3.7/site-packages/Nsound.py", line 14, in swig_import_helper
    return importlib.import_module(mname)
  File "/usr/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
  File "<frozen importlib._bootstrap>", line 983, in _find_and_load
  File "<frozen importlib._bootstrap>", line 967, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 670, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 583, in module_from_spec
  File "<frozen importlib._bootstrap_external>", line 1043, in create_module
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
ImportError: /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so: undefined symbol: PyInstance_Type

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/owner/.local/lib/python3.7/site-packages/Nsound.py", line 17, in <module>
    _Nsound = swig_import_helper()
  File "/home/owner/.local/lib/python3.7/site-packages/Nsound.py", line 16, in swig_import_helper
    return importlib.import_module('_Nsound')
  File "/usr/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
ImportError: /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so: undefined symbol: PyInstance_Type
```

The following show no matches:

```bash
grep 'PyInstance_Type' -r /home/owner/.local/lib/python3.7/site-packages --include \*.c
grep 'PyInstance_Type' -r /home/owner/.local/lib/python3.7/site-packages
grep "PyInstance_Type" -r /home/owner/.local/lib/python3.7/site-packages
grep "PyInstance_Type" -r /home/owner/.local/lib/python3.7
grep "swig_import_helper" -r /home/owner/.local/lib/python3.7
grep "swig_import_helper" -r /home/owner/.local/lib
grep "swig_import_helper" -r /usr/lib
```

The fault seems to be with swig (it is the only dependency not Python 2 specific that has calls from Python 2 and Python 3 < 3.6; though numpy also has the problem):
```
$ grep Py_InitModule -r /usr | grep -v 2.7
Binary file /usr/lib/x86_64-linux-gnu/samba/libsamba-net.so.0 matches
/usr/lib/python3/dist-packages/numpy/f2py/rules.py:\tm = #modulename#_module = Py_InitModule(\"#modulename#\", f2py_module_methods);
Binary file /usr/lib/python3/dist-packages/numpy/f2py/__pycache__/rules.cpython-37.pyc matches
/usr/share/swig3.0/python/pyinit.swg:  m = Py_InitModule((char *) SWIG_name, SwigMethods);
/usr/share/swig3.0/python/pyrun.swg:  PyObject *module = Py_InitModule((char*)"swig_runtime_data" SWIG_RUNTIME_VERSION, swig_empty_runtime_method_table);
```

```
$ grep --line-number PyInstance_Type -r /usr | grep -v 2.7
/usr/share/swig3.0/python/pyrun.swg:1409:  PyInstanceObject *inst = PyObject_NEW(PyInstanceObject, &PyInstance_Type);
```

After installing swig tarball (still has PyInstance_Type):
```bash
# grep Py_InitModule --line-number -r $HOME/Downloads/swig-4.0.2
grep Py_InitModule --line-number -r /usr/local | grep -v 2.7
# ^ OK (only has Python 3.5 & 2 stuff inside of cases for < 3):
#   /usr/local/share/swig/4.0.2/python/pyinit.swg:470:  m = Py_InitModule(SWIG_name, SwigMethods);
#   /usr/local/share/swig/4.0.2/python/pyrun.swg:1394:  PyObject *module = Py_InitModule("swig_runtime_data" SWIG_RUNTIME_VERSION, swig_empty_runtime_method_table);
grep PyInstance_Type --line-number -r $HOME/Downloads/swig-4.0.2
# ^ OK (no results)
```

and still has the error:
```python
>>> import Nsound as ns
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/owner/.local/lib/python3.7/site-packages/Nsound.py", line 15, in <module>
    import _Nsound
ImportError: /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so: undefined symbol: PyInstance_Type
```
- (PyInstance_Type is not used in the nsound code itself in the Poikilos fork; the problem may be added while pip builds the module--it may insert bad parts of swig tarball that still use `PyInstance_Type`).

So try:
```bash
grep Py_InitModule --line-number -r /home/owner/.local/lib | grep -v 2.7
# ^ uh oh:
#   Binary file /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so matches
grep PyInstance_Type --line-number -r /home/owner/.local/lib | grep -v 2.7
# ^ uh oh:
#   Binary file /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so matches
grep PyInstance_Type --line-number -r /home/owner/.local | grep -v 2.7
# ^ uh oh:
#   Binary file /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so matches
grep PyInstance_Type --line-number -r /usr/local
# ^ OK (no matches)
# Try uninstall then reinstall local version then:
grep PyInstance_Type --line-number -r /home/owner/.local/lib | grep -v 2.7
# ^ uh oh:
#   Binary file /home/owner/.local/lib/python3.7/site-packages/_Nsound.cpython-37m-x86_64-linux-gnu.so matches
```
