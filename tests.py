#!/usr/bin/env python
from gcodesynth.gcodesynth import GCodeSynth

gs = GCodeSynth()

# middle C is C4
# See <https://web.archive.org/web/20210313201509/
# https://pages.mtu.edu/~suits/notefreqs.html>

gs.push_line("M300 S440 P250")  # This is A4 (C4 is lower: range starts at C)
gs.push_line("M300 P500 S880  ; this is A5")
gs.push_line("M300 S932.33 P250 //this is A#5")
gs.push_line(" //this is a double slash comment on its own line")
gs.push_line(" ;this is a semicolon comment on its own line")
gs.dump()
gs.play()
