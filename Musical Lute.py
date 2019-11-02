import ctypes
import sys

ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "scripts/main.py 2 4 3", None, 1)
