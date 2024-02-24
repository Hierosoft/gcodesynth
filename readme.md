# gcodesynth
Play back G-code M300 music in Python 3 using pyaudio!

The actual codes are M-codes in this case.


## Install
(tested on Debian 10 Buster)
```bash
# sudo apt install -y python3-pip-autoremove
# ^ (optional) The command for the Python 3 version is `pip3-autoremove`.
# sudo apt install -y libportaudiocpp0 portaudio19-dev
# ^ Only necessary if using pip since pip would have to build the Python module from C.
sudo apt install -y python3-pyaudio
# ^ installs libportaudio2
mkdir -p ~/git
if [ ! -d ~/git/gcodesynth ]; then
    git clone https://github.com/poikilos/gcodesynth.git ~/git/gcodesynth
else
    cd ~/git/gcodesynth && git pull
fi
```


## Use
Try it out:
- Change to directory as shown in "Install" steps above.
- Download a gcode file such as found on a web search of: M300 music example
- Open a terminal (or Windows Command Prompt if you manage to get pyaudio installed)
- Run `python3 gcodesynth/playgcode.py $HOME\Downloads\something.gcode`
  (but change `$HOME\Downloads\something.gcode` to the file you downloaded.
  - Except if you are able to install using `cd ~/git && pip install --user gcodesynth`: then you can just use the `gcodesynth` command from any location instead of `cd ~/git/gcodesynth` and `python3 gcodesynth/playgcode.py`


## Developer Notes
See also [did_not_work.md][doc/development/did_not_work.md]


## Tags
audio music sound gcode g-code gcode-paser tone-generation tone-generator m300 commands
