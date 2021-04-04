#!/usr/bin/env python
from gcodesynth.gcodesynth import GCodeSynth


gs = GCodeSynth()

# middle C is C4
# See <https://web.archive.org/web/20210313201509/
# https://pages.mtu.edu/~suits/notefreqs.html>

gs.pushLine("M300 S440 P250") # This is A4
gs.pushLine("M300 P500 S880  ; this is A5")
gs.pushLine("M300 S932.33 P250 //this is A#5")
gs.pushLine(" //this is a double slash comment on its own line")
gs.pushLine(" ;this is a semicolon comment on its own line")
gs.dump()
gs.play()
