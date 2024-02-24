#!/usr/bin/env python

import sys
# import os

from gcodesynth.gcodecommand import GCodeCommand


class GCodeSynth():
    def __init__(self):
        GCodeCommand.start()
        self._commands = []

    def stop(self):
        GCodeCommand.stop()

    def clear(self):
        self._commands.clear()

    def push_line(self, gcode):
        self._commands.append(GCodeCommand(gcode.rstrip("\n\r")))

    def dump(self):
        for cmd in self._commands:
            print(cmd)

    def load(self, path):
        with open(path, 'r') as ins:
            for _raw in ins:
                self.push_line(_raw)
                # ^ does rstrip("\n\r")

    def play(self, log_level=0):
        missed = 0
        for cmd in self._commands:
            if cmd.is_comment():
                continue
            if cmd.is_blank():
                continue
            if not cmd.play(log_level=log_level):
                missed += 1
        return missed


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise ValueError("Provide either 1 (file) or 0 argument(s).")
    if len(sys.argv) > 1:
        gs = GCodeSynth()
        gs.load(sys.argv[1])
        gs.play()
