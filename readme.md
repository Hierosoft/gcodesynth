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
The program plays a sine wave sound from a G-code M300 command.

Run a sound test (See also "Play a single tone" further down):
- Close/stop/mute other programs that are using sound (or playback will stutter & lag severely).
- Open a terminal (or Windows Command Prompt if you manage to get pyaudio installed)
- Change to directory as shown in "Install" steps above.
- `cd tests`
- `python3 test_scales.py`

Run a file:
- Close/stop/mute other programs that are using sound (or playback will stutter & lag severely).
- Open a terminal (or Windows Command Prompt if you manage to get pyaudio installed)
- Change to directory as shown in "Install" steps above.
- Download any .gcode (G-code) file that has M300 commands such as found on a web search of: M300 music example
- Run `python3 gcodesynth/playgcode.py $HOME\Downloads\something.gcode`
  (but change `$HOME\Downloads\something.gcode` to the file you downloaded.
  - Except if you are able to install using `cd ~/git && pip install --user gcodesynth`: then you can just use the `gcodesynth` command from any location instead of `cd ~/git/gcodesynth` and `python3 gcodesynth/playgcode.py`

Play a single tone (does not require a G-code file):
- Close/stop other programs that are using sound (or playback will stutter & lag severely).
- Open a terminal (or Windows Command Prompt if you manage to get pyaudio installed)
- Change to directory as shown in "Install" steps above.
- Pass an M300 command to the gcodecommand script such as `python3 gcodesynth/gcodecommand.py M300 S440 P250`
  where:
  - `S440` says to use 440Hz ("A" in the musical scale using the A440 standard. See [Scientific pitch notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation#cite_note-JASA-6) on wikipedia, though the chart there uses the A440 standard not "[Scientific pitch](https://en.wikipedia.org/wiki/Scientific_pitch#cite_ref-1)" itself.)
  - `P250` says to play for 250 milliseconds (1/4 of a second).
  - See <https://marlinfw.org/docs/gcode/M300.html> for further instructions.
  - Except if you are able to install using `cd ~/git && pip install --user gcodesynth`: then you can just use the `gcodesynth-line` command from any location instead of `cd ~/git/gcodesynth` and `python3 gcodesynth/gcodecommand.py`


## Developer Notes
See also [did_not_work.md][doc/development/did_not_work.md]


## Tags
audio music sound gcode g-code gcode-paser tone-generation tone-generator m300 commands
