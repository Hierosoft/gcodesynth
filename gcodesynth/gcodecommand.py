#!/usr/bin/env python
import os
import sys

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
    from gcodesynth.gcodeparam import GCodeParam
except ImportError as ex:
    print("[gcodecommand] adjusting paths due to " + str(ex))
    repoDir = os.path.dirname(myDir)
    if not os.path.isdir(os.path.join(repoDir, "gcodesynth")):
        repoDir = os.path.dirname(repoDir)
        print("[gcodecommand] automatically changed repoDir to {}"
              "".format(repoDir))

    if not os.path.isdir(os.path.join(repoDir, "gcodesynth")):
        raise RuntimeError("[gcodecommand] gcodesynth wasn't in \"{}\""
                          "".format(repoDir))
    moduleDir = os.path.join(repoDir, "gcodesynth")
    sys.path.insert(0, repoDir)
    sys.stderr.write("[gcodecommand] trying from \"{}\"..."
                     "".format(repoDir))
    from gcodesynth.gcodeparam import GCodeParam
    sys.stderr.write("OK\n")



enable_audiogen = False
try:
    import audiogen_p3 as audiogen
    enable_audiogen = True
except ImportError:
    try:
        import audiogen
        enable_audiogen = True
    except ImportError:
        pass
print("enable_audiogen={}".format(enable_audiogen))
if not enable_audiogen:
    print("* audiogen is not available in your installation of Python"
          " {}".format(sys.version))

class GCodeCommand():
    '''
    Members:
    _ready -- Is it ready?
    _command -- (deprecated)
                It is a command if present (but params are in _params).
    _params -- This is a list of GCodeParam objects. The first is the
               command such as M300.
    _comments -- The comment at the end of the line (If _ready is True
                 and getCommand is None, the line is only a comment).
    '''

    def __init__(self, gcodeStr):
        '''
        Sequential arguments:
        gcodeStr -- a line of G-code (see loadLine), otherwise None.
        '''
        self._ready = False
        # self._command = None
        self._params = []
        self._comment = None
        if gcodeStr is not None:
            self.loadLine(gcodeStr)

    def getCommand(self):
        if len(self._params) < 1:
            return None
        return self._params[0]

    def getCommandStr(self):
        if len(self._params) < 1:
            return None
        return str(self.getCommand())

    def loadLine(self, gcodeStr):
        '''
        gcodeStr -- a line of G-code
        '''
        if not isinstance(gcodeStr, str):
            raise ValueError("A string is required.")
        if self._ready:
            raise RuntimeError("The GCodeCommand was already loaded.")
        if len(self._params) > 0:
            raise RuntimeError("The params were already loaded.")
        gcodeStrip = gcodeStr.strip()
        if gcodeStrip.startswith("//") or gcodeStrip.startswith(";"):
            self._command = None
            self._comment = gcodeStr
            self._ready = True
            return
        commentI1 = gcodeStr.find("//")
        commentI2 = gcodeStr.find(";")
        commentI = -1
        if (commentI1 > -1) and (commentI2 > -1):
            commentI = commentI1 if commentI1 < commentI2 else commentI2
        elif commentI1 > -1:
            commentI = commentI1
        elif commentI2 > -1:
            commentI = commentI2
        if commentI > -1:
            gcodeStrip = gcodeStr[:commentI].strip()

        if ("(" in gcodeStrip) or (">" in gcodeStrip):
            raise ValueError("inter-line comments are not implemented")

        parts = gcodeStrip.split()
        for i in range(len(parts)):
            part = parts[i]
            self._params.append(GCodeParam(part))

        self._ready = True

    def __repr__(self):
        if not self._ready:
            raise RuntimeError("The command was used before ready.")
        s = self.getCommandStr()
        if self._comment is not None:
            if s is None:
                return self._comment
        if s is None:
            raise RuntimeError("The command was None when ready.")
        s = ""
        for param in self._params:
            if param is None:
                raise RuntimeError("The command {} had a param that was"
                                   " None (got \"{}\" so far)."
                                   "".format(self._command, s))
            s += " " + str(param)
        if self._comment is not None:
            s += self._comment
        return s

    def isComment(self):
        return (self._comment is not None) and (len(self._params) < 1)

    def play(self):
        if not self._ready:
            raise RuntimeError("The command was played before ready.")
        if self.isComment():
            print("You tried to play a comment: {}"
                  "".format(self._comment))
            return
        if len(self._params) < 1:
            raise RuntimeError("There was no command during play.")
        if len(self._params) < 2:
            raise RuntimeError("There were no params during play"
                               " \"\"".format(str(self)))
        cmd = self._params[0]
        if cmd._n != "M":
            return
        if cmd._v != 300:
            return
        ms = self.getValue("P")
        Hz = self.getValue("S")
        print("* play {}ms {}Hz".format(ms, Hz))
        if not enable_audiogen:
            print("  enable_audiogen={}".format(enable_audiogen))
            return
        audiogen.sampler.play(audiogen.beep(
            frequency=Hz,
            seconds=float(ms)/1000,
        ))

    def getValue(self, char):
        return self.getParam(char)._v

    def getParam(self, char):
        if len(char) != 1:
            raise ValueError("Only one character was expected.")
        for i in range(1, len(self._params)):
            param = self._params[i]
            if param._n == char:
                return param

        raise KeyError("There was no param '{}' in \"{}\""
                       "".format(char, str(self)))

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        gc = GCodeCommand(" ".join(sys.argv[1:]))
        gc.play()

