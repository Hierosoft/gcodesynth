#!/usr/bin/env python
import os
import sys

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
    from gcodesynth.gcodeparam import GCodeParam
except ImportError as ex:
    print("[gcodecommand] adjusting paths due to " + str(ex))
    REPO_DIR = os.path.dirname(MY_DIR)
    if not os.path.isdir(os.path.join(REPO_DIR, "gcodesynth")):
        REPO_DIR = os.path.dirname(REPO_DIR)
        print("[gcodecommand] automatically changed REPO_DIR to {}"
              "".format(REPO_DIR))

    if not os.path.isdir(os.path.join(REPO_DIR, "gcodesynth")):
        raise RuntimeError("[gcodecommand] gcodesynth wasn't in \"{}\""
                           "".format(REPO_DIR))
    MODULE_DIR = os.path.join(REPO_DIR, "gcodesynth")
    sys.path.insert(0, REPO_DIR)
    sys.stderr.write("[gcodecommand] trying from \"{}\"..."
                     "".format(REPO_DIR))
    from gcodesynth.gcodeparam import GCodeParam
    sys.stderr.write("OK\n")


ENABLE_AUDIOGEN = False
try:
    import audiogen_p3 as audiogen
    ENABLE_AUDIOGEN = True
except ImportError:
    try:
        import audiogen
        ENABLE_AUDIOGEN = True
    except ImportError:
        pass
print("ENABLE_AUDIOGEN={}".format(ENABLE_AUDIOGEN))
if not ENABLE_AUDIOGEN:
    print("* audiogen is not available in your installation of Python"
          " {}".format(sys.version))


class GCodeCommand():
    '''
    Attributes:
        _ready (bool): Is it ready?
        _command (str): (deprecated) It is a command if present (but
            params are in _params).
        _params (list[GCodeParam]): This is a list of GCodeParam
            objects. The first is the command such as M300.
        _comment (str): The comment at the end of the line (If _ready is
            True and get_command is None, the line is only a comment).
    '''

    def __init__(self, gcode_raw):
        '''
        Sequential arguments:
        gcode_raw -- a line of G-code (see load_line), otherwise None.
        '''
        self._ready = False
        # self._command = None
        self._params = []
        self._comment = None
        if gcode_raw is not None:
            self.load_line(gcode_raw)

    def get_command(self):
        if len(self._params) < 1:
            return None
        return self._params[0]

    def get_command_str(self):
        if len(self._params) < 1:
            return None
        return str(self.get_command())

    def load_line(self, gcode_raw):
        '''
        Args:
            gcode_raw (str): a line of G-code (may contain newline
                character(s))
        '''
        if not isinstance(gcode_raw, str):
            raise ValueError("A string is required.")
        if self._ready:
            raise RuntimeError("The GCodeCommand was already loaded.")
        if len(self._params) > 0:
            raise RuntimeError("The params were already loaded.")
        gcode = gcode_raw.strip()
        if gcode.startswith("//") or gcode.startswith(";"):
            self._command = None
            self._comment = gcode_raw
            self._ready = True
            return
        comment_i1 = gcode_raw.find("//")
        comment_i2 = gcode_raw.find(";")
        comment_i = -1
        if (comment_i1 > -1) and (comment_i2 > -1):
            comment_i = comment_i1 if comment_i1 < comment_i2 else comment_i2
        elif comment_i1 > -1:
            comment_i = comment_i1
        elif comment_i2 > -1:
            comment_i = comment_i2
        if comment_i > -1:
            gcode = gcode_raw[:comment_i].strip()

        if ("(" in gcode) or (">" in gcode):
            raise ValueError("inter-line comments are not implemented")

        parts = gcode.split()
        for i in range(len(parts)):
            part = parts[i]
            self._params.append(GCodeParam(part))

        self._ready = True

    def __repr__(self):
        if not self._ready:
            raise RuntimeError("The command was used before ready.")
        s = self.get_command_str()
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

    def is_comment(self):
        return (self._comment is not None) and (len(self._params) < 1)

    def play(self):
        if not self._ready:
            raise RuntimeError("The command was played before ready.")
        if self.is_comment():
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
        ms = self.get_value("P")
        hz = self.get_value("S")
        print("* play {}ms {}Hz".format(ms, hz))
        if not ENABLE_AUDIOGEN:
            print("  ENABLE_AUDIOGEN={}".format(ENABLE_AUDIOGEN))
            return
        audiogen.sampler.play(audiogen.beep(
            frequency=hz,
            seconds=float(ms)/1000,
        ))

    def get_value(self, char):
        return self.get_param(char)._v

    def get_param(self, char):
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
