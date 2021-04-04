#!/usr/bin/env python

import sys
import os


myDir = os.path.dirname(os.path.realpath(__file__))
repoDir = myDir
moduleDir = os.path.join(repoDir, "gcodesynth")
try:
    import gcodesynth
    # ^ Assert that this isn't the repo directory (The repo isn't a
    #   module, so the script will stop here if the PATH is wrong).
    if not os.path.isdir(os.path.join(repoDir, "gcodesynth")):
        repoDir = os.path.dirname(repoDir)
    moduleDir = os.path.join(repoDir, "gcodesynth")
    sys.path.insert(0, repoDir)
    from gcodesynth.gcodecommand import GCodeCommand
except ImportError as ex:
    print("[gcodesynth] adjusting paths due to " + str(ex))
    repoDir = os.path.dirname(myDir)
    if not os.path.isdir(os.path.join(repoDir, "gcodesynth")):
        repoDir = os.path.dirname(repoDir)
        print("[gcodecommand] automatically changed repoDir to {}"
              "".format(repoDir))

    if not os.path.isdir(os.path.join(repoDir, "gcodesynth")):
        raise RuntimeError("[gcodesynth] gcodesynth wasn't in \"{}\""
                          "".format(repoDir))
    moduleDir = os.path.join(repoDir, "gcodesynth")
    sys.path.insert(0, repoDir)
    sys.stderr.write("[gcodesynth] trying from \"{}\"..."
                     "".format(repoDir))
    from gcodesynth.gcodecommand import GCodeCommand
    sys.stderr.write("OK\n")



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
