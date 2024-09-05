#%%
import random
import numpy

#%%
# Define chords for each melody note (as chromatic offsets with 0 being the base note)
chord_dict = {
    0: [[0, 4, 7]], # Major chord (I) including second inversion (I6/4)
    1: [[1, 5, 8]], # Minor chord (♭II)
    2: [[2, 5, 9], [0, 4, 7, 2], [0, 2, 7]], # Minor chord (ii), 9th chord, sus2 chord
    3: [[3, 7, 10], [0, 3, 7, 10]], # Minor chord (♭III), Minor 7th chord (m7)
    4: [[4, 7, 11], [0, 5, 7]], # Minor chord (iii), Suspended 4th chord (sus4)
    5: [[5, 9, 0]], # Major chord (IV)
    6: [[6, 10, 1]], # Major chord (IV#)
    7: [[7, 11, 2]], # Major chord (V)
    8: [[8, 0, 3], [0, 4, 8]], # Major chord (♭VI), Augmented chord (aug)
    9: [[9, 0, 4]], # Minor chord (vi)
    10: [[10, 1, 5], [10, 2, 7]], # Minor chord (♭vii), Dominant 7th suspended 4th (7sus4)
    11: [[11, 2, 5]], # Diminished chord (vii°)
    }

#%%
def note_to_chromatic(note_name):
    # Define a mapping of note names to chromatic scale positions
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    if note_name in chromatic_scale:
        return chromatic_scale.index(note_name)
    else:
        # Check for flat (♭) or sharp (#) accidentals
        if '♭' in note_name:
            note_name = note_name.replace('♭', 'b')
        elif '#' in note_name:
            note_name = note_name.replace('#', '')
        
        if note_name in chromatic_scale:
            return chromatic_scale.index(note_name)
        else:
            return None

def chromatic_to_note(chromatic_offset):
    # Define a mapping of chromatic offsets to note names
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    return chromatic_scale[chromatic_offset]

def transpose_chord(chord, key_offset):
    # Transpose the chord to the specified key
    transposed_chord = [(note + key_offset) % 12 for note in chord]
    return transposed_chord

#%%
# Function to transpose chords to a new key
def generate_chords(melody, key):
    # Define chord progressions for SATB voices
    soprano_chords = []
    alto_chords = []
    tenor_chords = []
    bass_chords = []

    # Convert user-defined key to a numeric offset
    key_offset = note_to_chromatic(key)

    if key_offset is None:
        raise ValueError("Invalid key name. Please use a valid note (e.g., C, D#, E)")

    # Define chords for each melody note (as chromatic offsets with 0 being the base note)
    chord_dict = {
        0: [[0, 4, 7]], # Major chord (I) including second inversion (I6/4)
        1: [[1, 5, 8]], # Minor chord (♭II)
        2: [[2, 5, 9], [0, 4, 7, 2], [0, 2, 7]], # Minor chord (ii), 9th chord, sus2 chord
        3: [[3, 7, 10], [0, 3, 7, 10]], # Minor chord (♭III), Minor 7th chord (m7)
        4: [[4, 7, 11], [0, 5, 7]], # Minor chord (iii), Suspended 4th chord (sus4)
        5: [[5, 9, 0]], # Major chord (IV)
        6: [[6, 10, 1]], # Major chord (IV#)
        7: [[7, 11, 2]], # Major chord (V)
        8: [[8, 0, 3], [0, 4, 8]], # Major chord (♭VI), Augmented chord (aug)
        9: [[9, 0, 4]], # Minor chord (vi)
        10: [[10, 1, 5], [10, 2, 7]], # Minor chord (♭vii), Dominant 7th suspended 4th (7sus4)
        11: [[11, 2, 5]], # Diminished chord (vii°)
    }

    for note_name in melody:
        # Get the list of chord definitions associated with the note
        chord_definitions = chord_dict.get(note_to_chromatic(note_name), [[note_to_chromatic(note_name)]])

        # Randomly select one chord definition
        selected_chord = random.choice(chord_definitions)

        # Transpose the chord to match the specified key
        transposed_chord = transpose_chord(selected_chord, key_offset)

        # Determine the melody note in the chord
        melody_chord_note = chromatic_to_note(note_to_chromatic(note_name))

        # Ensure that the melody note is at least present in one part (SATB)
        soprano_chords.append(melody_chord_note) # Soprano gets to melody part
        alto_chords.append(random.choice(transposed_chord))
        tenor_chords.append(random.choice(transposed_chord))
        bass_chords.append(random.choice(transposed_chord))

    return soprano_chords, alto_chords, tenor_chords, bass_chords
#%%

# Input the musical key and melody from the user
key = input("Enter the musical key (e.g., C, D#, E): ")
melody = input("Enter the melody line (e.g., D F# A D): ").split()

# Generate and display the chords
soprano, alto, tenor, bass = generate_chords(melody, key)

# Convert numerical notes to alphabet
soprano_str = [chromatic_to_note(note) if isinstance(note, int) else note for note in soprano]
alto_str = [chromatic_to_note(note) if isinstance(note, int) else note for note in alto]
tenor_str = [chromatic_to_note(note) if isinstance(note, int) else note for note in tenor]
bass_str = [chromatic_to_note(note) if isinstance(note, int) else note for note in bass]

# Print the results with improved alignment
print("Soprano:", " ".join(soprano_str))
print("Alto:   ", " ".join(alto_str))
print("Tenor:  ", " ".join(tenor_str))
print("Bass:   ", " ".join(bass_str))

#%%
# Define a dictionary to map rhythm notations to durations
rhythm_durations = {
    "oo": 4.0,    # Whole note
    "o": 2.0,     # Half note
                  # Quarter note need not add any symbol
    ")": 0.5,     # Eighth note
    "))": 0.25,   # Sixteenth note 
}

#%%
# Input melody line with rhythm notation
melody_with_rhythm = "C E G | C D. G) | Co C | Go."

#%%
# Function to calculate note duration based on rhythm notation, including dotted rhythms
def get_note_duration(note_with_rhythm):
    base_duration, dot = note_with_rhythm.split(".") if "." in note_with_rhythm else (note_with_rhythm, "")
    duration = rhythm_durations.get(base_duration, 1.0)
    if dot:
        duration *= 1.5  # Dotted rhythm (increases duration by 1.5 times)
    return duration
# Debug print to check the notes_with_rhythm
print("Notes with Rhythm:", melody_with_rhythm)
# Transpose the universal chord progressions to the user's selected key
chord_progressions_in_key = transpose_chord(universal_cchord_progressions, 0, user_key)


#%%

from music21 import stream, note

# Create a music21 Stream to hold the SATB parts
music_score = stream.Score()

# Create separate music21 Streams for each voice
soprano_part = stream.Part()
alto_part = stream.Part()
tenor_part = stream.Part()
bass_part = stream.Part()

# Add the SATB parts to their respective streams
for chord, duration in soprano:
    soprano_part.append(note.Note(chord[0], duration=duration))
for chord, duration in alto:
    alto_part.append(note.Note(chord[0], duration=duration))
for chord, duration in tenor:
    tenor_part.append(note.Note(chord[0], duration=duration))
for chord, duration in bass:
    bass_part.append(note.Note(chord[0], duration=duration))

# Append the voice parts to the main score
music_score.append(soprano_part)
music_score.append(alto_part)
music_score.append(tenor_part)
music_score.append(bass_part)

# Show the music score (or export it to a file)
music_score.show()

#%%