# gcodesynth
Play back G-code M300 music in Python 3 using audiogen_p3!

The actual codes are M-codes in this case.


## Install
(tested on Debian 10 Buster)
```
# sudo apt install -y python3-pip-autoremove
# ^ (optional) The command for the Python 3 version is `pip3-autoremove`.
sudo apt install -y libportaudiocpp0 portaudio19-dev
python3 -m pip install https://github.com/rguisewite/audiogen_p3/archive/refs/heads/master.zip
mkdir -p ~/git
if [ ! -d ~/git/gcodesynth ]; then
    git clone https://github.com/poikilos/gcodesynth.git ~/git/gcodesynth
else
    cd ~/git/gcodesynth && git pull
fi
```


## Developer Notes
2021-04-04 I e-mailed the PyAudiere author to request he places PyAudiere on GitHub.

See also improved audiogen_p3 documentation at https://github.com/rguisewite/audiogen_p3/pull/1

### audiogen usage
(guesswork based on examples)
```Python
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
```
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
# sudo apt install -y python3-pyaudio
# pip3-autoremove audiogen_p3
python3 -m pip install https://github.com/rguisewite/audiogen_p3/archive/refs/heads/master.zip

# See also: another fork with more tests and similar Python 3 fixes: <https://github.com/gdusbabek/audiogen>


# ^ from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# found via <https://stackoverflow.com/questions/54998028/how-do-i-install-pyaudio-on-python-3-7>

```

### Fixing audiogen

```
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

```
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

```
sudo apt install -y scons swig libportaudiocpp0 portaudio19-dev
# python2 -m pip install --user nsound
# ^ python2 only
# python3 -m pip install --user https://github.com/weegreenblobbie/nsound/archive/refs/heads/master.zip
# ^      File "/tmp/pip-req-build-7vqdghi2/setup.py", line 190, in process_nsound_h
#          keys.sort()
#      AttributeError: 'dict_keys' object has no attribute 'sort'
# ^ until the following issue is resolved: <https://github.com/weegreenblobbie/nsound/issues/17>
# python3 -m pip install --user ~/git/nsound
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

```
owner@pgs:~$ grep 'PyInstance_Type' -r /home/owner/.local/lib/python3.7/site-packages --include \*.c
owner@pgs:~$ grep 'PyInstance_Type' -r /home/owner/.local/lib/python3.7/site-packages
owner@pgs:~$ grep "PyInstance_Type" -r /home/owner/.local/lib/python3.7/site-packages
owner@pgs:~$ grep "PyInstance_Type" -r /home/owner/.local/lib/python3.7
owner@pgs:~$ grep "swig_import_helper" -r /home/owner/.local/lib/python3.7
owner@pgs:~$ grep "swig_import_helper" -r /home/owner/.local/lib
owner@pgs:~$ grep "swig_import_helper" -r /usr/lib
```

## Tags
audio music sound gcode g-code gcode-paser tone-generation tone-generator m300 commands
