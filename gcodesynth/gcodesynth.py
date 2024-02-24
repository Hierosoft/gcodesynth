#!/usr/bin/env python

import sys
import os

MY_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = MY_DIR
MODULE_DIR = os.path.join(REPO_DIR, "gcodesynth")
try:
    import gcodesynth
    # ^ Assert that this isn't the repo directory (The repo isn't a
    #   module, so the script will stop here if the PATH is wrong).
    if not os.path.isdir(os.path.join(REPO_DIR, "gcodesynth")):
        REPO_DIR = os.path.dirname(REPO_DIR)
    MODULE_DIR = os.path.join(REPO_DIR, "gcodesynth")
    sys.path.insert(0, REPO_DIR)
    from gcodesynth.gcodecommand import GCodeCommand
except ImportError as ex:
    print("[gcodesynth] adjusting paths due to " + str(ex))
    REPO_DIR = os.path.dirname(MY_DIR)
    if not os.path.isdir(os.path.join(REPO_DIR, "gcodesynth")):
        REPO_DIR = os.path.dirname(REPO_DIR)
        print("[gcodecommand] automatically changed REPO_DIR to {}"
              "".format(REPO_DIR))

    if not os.path.isdir(os.path.join(REPO_DIR, "gcodesynth")):
        raise RuntimeError("[gcodesynth] gcodesynth wasn't in \"{}\""
                           "".format(REPO_DIR))
    MODULE_DIR = os.path.join(REPO_DIR, "gcodesynth")
    sys.path.insert(0, REPO_DIR)
    sys.stderr.write("[gcodesynth] trying from \"{}\"..."
                     "".format(REPO_DIR))
    from gcodesynth.gcodecommand import GCodeCommand
    sys.stderr.write("OK\n")


class GCodeSynth():
    def __init__(self):
        GCodeCommand.start()
        self._commands = []

    def stop(self):
        GCodeCommand.stop()

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

    def play(self):
        for cmd in self._commands:
            if cmd.is_comment():
                continue
            cmd.play()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise ValueError("Provide either 1 (file) or 0 argument(s).")
    if len(sys.argv) > 1:
        gs = GCodeSynth()
        gs.load(sys.argv[1])
        gs.play()
