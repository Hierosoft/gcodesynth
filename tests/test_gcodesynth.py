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
        cls = TestGCodeSynth
        path = os.path.join(TEST_DATA_DIR, "with_comments.gcode")
        cls.gs.clear()
        cls.gs.load(path)
        cls.gs.play()

    @classmethod
    def tearDownClass(cls):
        cls.gs.stop()


if __name__ == "__main__":
    unittest.main()