
from __future__ import division
from __future__ import print_function
import math
import pyaudio
# sudo apt install python-pyaudio
# sudo dnf install python3-pyaudio
# ^ install as package so compilation is not necessary,
#   otherwise build (such as pip install) would require:
# sudo apt install portaudio-dev
# sudo dnf install portaudio-devel


PyAudio = pyaudio.PyAudio
p = None


def start():
    global p
    if p is not None:
        raise RuntimeError("pyaudio was already initialized")
    p = PyAudio()


def stop():
    global p
    p.terminate()
    p = None


def play_8bit_sine(frequency, length=1, sample_rate=44100):
    '''Play a note at 8 bit sample resolution.
    8-bit is the "vertical" detail (256 levels in the case of 8-bit),
    whereas sample_rate is the timewise detail.

    Args:
        frequency (float): Hz, waves per second, 261.63=C4-note.
        length (float): seconds to play sound
        sample_rate (int): The number of samples per second.
    '''
    # Based on https://stackoverflow.com/a/33880295/4541104 by Liam
    # accessed May 30, 2022

    # sample_rate = max(sample_rate, frequency+100)
    # ^ This would help detail but subvert the caller's value

    frames_total = int(float(sample_rate) * length)
    # frames_remainder = frames_total % sample_rate
    wavedata = ''

    # Generate sine wave
    for x in range(frames_total):
        wavedata += (
            chr(round(math.sin(x/((sample_rate/frequency)/math.pi))*127+128))
        )
        # ^ round seems to improve the audio slightly at 8 bit
        #   regardless of sample rate, but more apparent at lower sample rates
    print("{} samples".format(frames_total))

    # for x in range(frames_remainder):
    #     wavedata += chr(128)

    try:
        stream = p.open(format=p.get_format_from_width(1),
                        channels=1,
                        rate=sample_rate,
                        output=True)

        stream.write(wavedata)
        stream.stop_stream()
    finally:
        stream.close()
