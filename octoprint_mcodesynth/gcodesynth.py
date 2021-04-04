#!/usr/bin/env python

import sys
import os


myDir = os.path.dirname(os.path.realpath(__file__))
repoDir = myDir
try:
    from octoprint_gcodesynth.gcodecommand import GCodeCommand
except ImportError as ex:
    print(str(ex))
    repoDir = os.path.dirname(myDir)
    sys.path.append(repoDir)
    print("Trying from \"{}\"...".format(repoDir))
    from octoprint_gcodesynth.gcodecommand import GCodeCommand



class GCodeSynth():
    def __init__(self):
        self._commands = []

    def pushLine(self, gcodeStr):
        self._commands.append(GCodeCommand(gcodeStr.rstrip("\n\r")))

    def dump(self):
        for cmd in self._commands:
            print(cmd)

    def load(self, path):
        with open(path, 'r') as ins:
            for rawL in ins:
                self.pushLine(rawL)
                # ^ does rstrip("\n\r")

    def play(self):
        for cmd in self._commands:
            if cmd.isComment():
                continue
            cmd.play()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise ValueError("Provide either 1 (file) or 0 argument(s).")
    if len(sys.argv) > 1:
        gs = GCodeSynth()
        gs.load(sys.argv[1])
        gs.play()