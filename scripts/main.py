import time
import output as out
import rtmidi
import ctypes
import sys


keyMap = {"C": 0x02, "D": 0x03, "E": 0x04, "F": 0x05, "G": 0x06, "A": 0x07, "B": 0x08, "N": 0x09}


def get_name(midi):
	return midi.getMidiNoteName(midi.getNoteNumber())


def release_all():
	for v in keyMap.values():
		out.release_key(v)


def play_note(note_raw):
	note = get_name(note_raw)
	if len(note) > 2:
		return
	
	if not MIN_OCTAVE <= int(note[1]) <= MAX_OCTAVE and not note == f"C{MAX_OCTAVE+1}":
		return
	
	if note_raw.isNoteOff():
		out.release_key(keyMap[note[0]])
		if note[0] == "C":
			out.release_key(keyMap["N"])
		return
	
	global curOctave
	while int(note[1]) != curOctave and note != f"C{curOctave+1}":
		global lastSwapTime
		while time.perf_counter() - lastSwapTime < 0.11:
			pass
		lastSwapTime = time.perf_counter()
		release_all()
		if int(note[1]) > curOctave:
			out.send_key(0x0B)
			curOctave += 1
		elif int(note[1]) < curOctave:
			out.send_key(0x0A)
			curOctave -= 1
	if note == f"C{curOctave + 1}":
		out.press_key(keyMap["N"])
	else:
		out.press_key(keyMap[note[0]])


if len(sys.argv) != 4 or not ctypes.windll.shell32.IsUserAnAdmin():
	print("\nRun the script corresponding to the instrument you want to play. Do not run this script directly.")
	input("\n\nPress Enter to continue...")
	sys.exit(1)


MIN_OCTAVE = int(sys.argv[1])
MAX_OCTAVE = int(sys.argv[2])
curOctave = int(sys.argv[3])

midiin = rtmidi.RtMidiIn()

lastSwapTime = time.perf_counter()


while midiin.getPortCount() == 0:
	input("\nPress Enter to retry...\n")
	midiin = rtmidi.RtMidiIn()

midiin.openPort(0)
midiin.setCallback(play_note)

input("\nPress Enter to quit...")
