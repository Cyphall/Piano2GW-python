import time
import output as out
import rtmidi
import ctypes
import sys


keyMap = {"C": 0x02, "D": 0x03, "E": 0x04, "F": 0x05, "G": 0x06, "A": 0x07, "B": 0x08, "S": 0x09}


def getName(midi):
	return midi.getMidiNoteName(midi.getNoteNumber())


def releaseAll():
	for v in keyMap.values():
		out.ReleaseKey(v)


def playNote(note_raw):
	note = list(note_raw.getMidiNoteName(note_raw.getNoteNumber()))
	if (len(note) > 2):
		return
	
	if (note == ["C", "5"]):
		note = ["S", "4"]
	
	if (not MIN_OCTAVE <= int(note[1]) <= MAX_OCTAVE):
		return
	
	if (note_raw.isNoteOff()):
		out.ReleaseKey(keyMap[note[0]])
		return
	
	global curOctave
	while(int(note[1]) != curOctave):
		releaseAll()
		if (int(note[1]) > curOctave):
			out.SendKey(0x0B)
			curOctave += 1
		elif (int(note[1]) < curOctave):
			out.SendKey(0x0A)
			curOctave -= 1
		time.sleep(0.01)
	out.PressKey(keyMap[note[0]])


if (len(sys.argv) != 4 or not ctypes.windll.shell32.IsUserAnAdmin()):
	print("\nRun the script corresponding to the instrument you want to play. Do not run this script directly.")
	input("\n\nPress Enter to continue...")
	sys.exit(1)


MIN_OCTAVE = int(sys.argv[1])
MAX_OCTAVE = int(sys.argv[2])
curOctave = int(sys.argv[3])

midiin = rtmidi.RtMidiIn()


while midiin.getPortCount() == 0:
	input("\nPress Enter to retry...\n")
	midiin = rtmidi.RtMidiIn()


midiin.openPort(0)

print("\nRunning...")

while True:
	if midiin.getPortCount() == 0:
		break
	n = midiin.getMessage()
	if n:
		playNote(n)
