#!/usr/bin/env python
import os
import sys
import unittest

if __name__ == "__main__":
    # Allow importing from nearby module if run without pytest
    TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(TESTS_DIR)
    TEST_DATA_DIR = os.path.join(TESTS_DIR, "data")
    sys.path.insert(0, REPO_DIR)

from gcodesynth import GCodeSynth

def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class TestGCodeSynth(unittest.TestCase):
    gs = None

    @classmethod
    def setUpClass(cls):
        cls.gs = GCodeSynth()

    def test_m300(self):
        cls = TestGCodeSynth
        cls.gs.clear()
        cls.gs.push_line("M300 S440 P250")  # ~A4 (C4 is lower & 1st 4)
        cls.gs.push_line("M300 P250 S880  ; A5")
        cls.gs.push_line("M300 S932.33 P250 //A#5")
        cls.gs.push_line(" //this is a double slash comment on its own line")
        cls.gs.push_line(" ;this is a semicolon comment on its own line")
        cls.gs.push_line("; A440 is the standard for the freqencies here")
        cls.gs.dump()
        cls.gs.play()

    def test_m300_file(self):
        log_level = 1
        cls = TestGCodeSynth
        name = "with_comments.gcode"
        path = os.path.join(TEST_DATA_DIR, name)
        cls.gs.clear()
        cls.gs.load(path)
        missed = cls.gs.play(log_level=log_level)
        echo0("{} unplayable line(s) in {}".format(missed, name))

    def test_blank_lines(self):
        log_level = 1
        cls = TestGCodeSynth
        name = "combine_1ms_tones.gcode"
        path = os.path.join(TEST_DATA_DIR, name)
        cls.gs.clear()
        cls.gs.load(path)
        missed = cls.gs.play(log_level=log_level)
        if missed > 0:
            echo0("{} unplayable line(s) in {}".format(missed, name))
            echo0("  (Should be 0 since play should not even try to play"
                  " lines that have no command)")
        self.assertEqual(missed, 0)

    @classmethod
    def tearDownClass(cls):
        cls.gs.stop()


if __name__ == "__main__":
    unittest.main()
