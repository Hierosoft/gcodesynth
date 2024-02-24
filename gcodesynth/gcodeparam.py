#!/usr/bin/env python


class GCodeParam():
    '''
    Attributes:
        _v (Union[int,float,str]): the value (converted to int, but if
            not possible, to float, or as a last resort, string)
        _n (str): the name
    '''

    def __init__(self, chunk):
        '''Load a chunk as the param.

        Args:
            chunk (str): A param string (see load) or None.
        '''
        self._ready = False
        self._n = None
        self._v = None
        if chunk is not None:
            self.load(chunk)

    def load(self, chunk):
        '''Load a chunk as the param.

        Args:
            chunk (str): The param string such as S300 (or a command
                such as M300).
        '''
        if not isinstance(chunk, str):
            raise ValueError("A string param is required.")
        if " " in chunk:
            raise ValueError("A G-code param must not contain spaces.")
        if ("(" in chunk) or (">" in chunk):
            raise ValueError("inter-line comments are not implemented")
        self._n = chunk[0:1]
        _s = chunk[1:]
        if len(_s) < 1:
            msg = "The param {} had no value.".format(chunk)
            # raise ValueError(msg)
            # This is not an error, since G-code allows "G28 X Y"
            print(msg)
            self._v = ""
        else:
            try:
                self._v = int(_s)
            except ValueError:
                try:
                    self._v = float(_s)
                except ValueError:
                    print("WARNING: {} became a string in {} (an int or"
                          " float is more common;"
                          "suffixes are not implemented in gcodeparam)."
                          "".format(_s, chunk))
                    self._v = _s
        self._ready = True

    def __repr__(self):
        if not self._ready:
            raise RuntimeError("The param was used before ready.")
        return "{}{}".format(self._n, self._v)

    def __str__(self):
        return self.__repr__()
