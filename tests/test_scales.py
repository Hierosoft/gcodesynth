import os
import sys
import unittest

if __name__ == "__main__":
    # Allow importing from nearby module if run without pytest
    TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(TESTS_DIR)
    sys.path.insert(0, REPO_DIR)


from gcodesynth.gcspyaudio import (
    start,
    play_8bit_sine,
    stop,
)
from gcodesynth.scales import SCALES


class TestGcodeSynth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        start()

    def test_play_8bit_sine(self):
        print("A4")
        play_8bit_sine(SCALES['A440']['A 4'], length=.25)
        print("C4")
        play_8bit_sine(SCALES['A440']['C 4'], length=.25)
        print("C3")
        play_8bit_sine(SCALES['A440']['C 3'])
        print("done")

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
