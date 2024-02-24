#!/usr/bin/env python
"""
Play a single G-code command (M300 play tone).

Usage:
gcodecommand.py M300 P153 S659
# where 659 is the pitch in Hz, and 153 is length in milliseconds
#   (default 1ms as per Marlin G-code docs:
#   <https://marlinfw.org/docs/gcode/M300.html>).
# NOTE: Counter-intuitively S is Hz, P is ms.
"""
import os
import sys

if __name__ == "__main__":
    # Allow importing from nearby module if run without pytest
    TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(TESTS_DIR)
    sys.path.insert(0, REPO_DIR)

from gcodesynth.gcodeparam import GCodeParam

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
# print("ENABLE_AUDIOGEN={}".format(ENABLE_AUDIOGEN))
if not ENABLE_AUDIOGEN:
    pass
    # print("* audiogen is not available in your installation of Python"
    #       " {}".format(sys.version))

def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if not ENABLE_AUDIOGEN:
    from gcodesynth.gcspyaudio import (
        play_8bit_sine,
        start,
        stop,
    )
else:
    def start():
        pass

    def stop():
        pass


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
        Args:
            gcode_raw (str): a line of G-code (see load_line), otherwise
                None.
        '''
        self._ready = False
        # self._command = None
        self._params = []
        self._comment = None
        if gcode_raw is not None:
            self.load_line(gcode_raw)

    @staticmethod
    def start():
        start()

    @staticmethod
    def stop():
        stop()

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

    def is_blank(self):
        '''Return whether this is not a command.
        The command is first param, so blank only if nothing in _params.
        '''
        return not self._params

    def play(self, log_level=0):
        if not self._ready:
            raise RuntimeError("The command was played before ready.")
        if self.is_comment():
            print("You tried to play a comment: {}"
                  "".format(self._comment))
            return False
        if len(self._params) < 1:
            echo0("Warning: tried to play a blank command")
            return False
        if len(self._params) < 2:
            raise RuntimeError("There were no params during play"
                               " \"{}\"".format(str(self)))
        cmd = self._params[0]
        if cmd._n != "M":
            return False
        if cmd._v != 300:
            return False
        # See <https://marlinfw.org/docs/gcode/M300.html>
        ms = 1  # default is 1 millisecond as per Marlin G-code docs
        if self.has_param('P'):  # P is ms *not* pitch
            ms = self.get_value('P')
        else:
            # if log_level > 0:
            echo0("Warning: inaudible (Defaulting to {}ms"
                  ", P not specified)".format(ms))
        hz = 260  # default is 260 as per Marlin G-code docs
        if self.has_param('S'):
            hz = self.get_value('S')  # S is Hz *not* ms
        if log_level > 0:
            echo0("* play {}ms {}Hz".format(ms, hz))
        if not ENABLE_AUDIOGEN:
            # print("  ENABLE_AUDIOGEN={}".format(ENABLE_AUDIOGEN))
            play_8bit_sine(
                hz,
                length=float(ms)/1000,
                log_level=log_level,
            )
            return True
        audiogen.sampler.play(audiogen.beep(
            frequency=hz,
            seconds=float(ms)/1000,
        ))
        return True

    def get_value(self, char):
        return self.get_param(char)._v

    def has_param(self, char):
        for param in self._params:
            if param._n == char:
                return True
        return False

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


def usage():
    echo0(__doc__)


def main():
    if len(sys.argv) > 1:
        start()
        gc = GCodeCommand(" ".join(sys.argv[1:]))
        played = gc.play()
        stop()
        if not played:
            usage()
            echo0("Error: There was no playable M300 command.")
            return 1
    else:
        usage()
        echo0("Error: There was no M300 command specified.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
