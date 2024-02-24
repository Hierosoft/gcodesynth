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


## Developer Notes
See also [did_not_work.md][doc/development/did_not_work.md]


## Tags
audio music sound gcode g-code gcode-paser tone-generation tone-generator m300 commands
