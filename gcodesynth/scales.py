'''
A440 frequencies are from the table at
https://en.wikipedia.org/wiki/Scientific_pitch_notation. The article
also says:
"Mathematically, given the number n of semitones above middle C, the
fundamental frequency in hertz is given by 440 * 2 ^ (( n − 9 ) / 12)
(see [twelfth root of
two](https://en.wikipedia.org/wiki/Twelfth_root_of_two "Twelfth root of
two")). Given the MIDI NoteOn number m, the frequency of the note is
normally  440 * 2 ^ (( m − 69 )  /  12) Hz, using standard tuning."

and:

"With changes in concert pitch and the widespread adoption of A440 as
a musical standard, new scientific frequency tables were published by
the Acoustical Society of America in 1939, and adopted by the
International Organization for Standardization in 1955. C0, which was
exactly 16 Hz under the scientific pitch standard, is now 16.352 Hz
under the current international standard system.[6]"

6.  Young, Robert W. (1939). "Terminology for Logarithmic Frequency
Units". Journal of the Acoustical Society of America. 11 (1): 134–000.
Bibcode:1939ASAJ...11..134Y. doi:10.1121/1.1916017.

and:

"both Yamaha and the software MaxMSP define middle C as C3. Apple's
GarageBand also defines middle C (261.6256 Hz) as C3."

Middle C is C4
See <https://web.archive.org/web/20210313201509/
https://pages.mtu.edu/~suits/notefreqs.html>

'''
import csv
import os

SCALES = {}

# INFO: for scientific pitch notation see
#   <https://en.wikipedia.org/wiki/Scientific_pitch_notation>
# A440_FREQS = {  # A440 was widely adopted in 1939
#     "C0": 16.35160,  # sub-contra octave
#     "A4": 440,
#     "C4": 261.63,  # Middle C (C4 in scientific pitch notation)
# }

# NOTE: C4 is *lower* than A4 because numbers increment at C.

SP_FREQS = {  # Though all dicts here are "scientific pitch notation",
    # only this one is "Scientific Pitch"! They are not the same.
    "C -4": 1,
    "C -3": 2,
    "C -2": 4,
    "C -1": 8,
    "C 0": 16,
    "C 1": 32,
    "C 2": 64,
    "C 3": 128,
    "C 4": 256,  # Middle C
    "C 5": 512,
    "C 6": 1024,
    "C 7": 2048,
    "C 8": 4096,
    "C 9": 8192,
    "C 10": 16384,
    "C 11": 32768,
    "C 12": 65536,
}

GARAGEBAND_FREQS = {  # See wikipedia.org/wiki/Scientific_pitch_notation
    "C 3": 261.6256,  # Notice that usually this is C4: Garage Band is annoying
}


SCALES['A440'] = {}  # A440_FREQS
SCALES['scientific pitch'] = SP_FREQS
SCALES['garageband'] = GARAGEBAND_FREQS
MIDI_NOTE_NUMS = {}
MIDI_NOTE_NUMS = []
for _ in range(128):
    MIDI_NOTE_NUMS.append(None)  # filled in below

scale_a440_name = 'scale-A440.csv'
MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(MODULE_PATH, "data")
scale_a440_path = os.path.join(DATA_PATH, scale_a440_name)

with open(scale_a440_path) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = None
    for row in csv_reader:
        if header is None:
            print("type(row)={}".format(type(row).__name__))
            header = row
            continue
        note_names = None
        for i, field in enumerate(row):
            column_name = header[i]
            if i == 0:
                note_names = row[0].split("/")
                continue
            print("loading {}".format(field))
            end_i = field.find("(")
            midi_note_num = None  # 0 to 127
            if end_i > 0:
                pitch_str = field[:end_i-1].strip()
                midi_note_num_s = field[end_i+1:].strip(")").strip()
                print("  midi_note_num: {}".format(midi_note_num_s))
                midi_note_num = int(midi_note_num_s)
            else:
                pitch_str = field
            print("  pitch: {}".format(pitch_str))
            pitch = float(pitch_str)
            if midi_note_num:
                MIDI_NOTE_NUMS[midi_note_num]
            for note_name in note_names:
                note_and_number = note_name.strip() + " " + str(column_name)
                # ^ Examples:
                #   - "C sharp 4" (and same pitch for "D flat 4")
                #   - "C 4"
                print("  note_and_number: {}".format(note_and_number))
                SCALES['A440'][note_and_number] = pitch
        SCALES['A440']
