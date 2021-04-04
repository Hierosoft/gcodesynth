#!/usr/bin/env python

from octoprint_gcodesynth.gcodecommand import GCodeCommand

class GCodeSynth():
    def __init__(self):
        self._commands = []

    def pushLine(self, gcodeStr):
        self._commands.append(GCodeCommand(gcodeStr))

    def dump(self):
        for cmd in self._commands:
            print(cmd)

    def play(self):
        for cmd in self._commands:
            if cmd.isComment():
                continue
            cmd.play()
