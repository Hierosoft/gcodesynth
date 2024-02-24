import os
import sys


if __name__ == "__main__":
    # Allow importing from nearby module if run without pytest
    TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(TESTS_DIR)
    sys.path.insert(0, REPO_DIR)

from gcodesynth import GCodeSynth

gs = None


def main():
    global gs

    if len(sys.argv) != 2:
        raise ValueError("Provide either 1 (file) or 0 argument(s).")

    gs = GCodeSynth()
    gs.load(sys.argv[1])
    gs.play()
    gs.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())