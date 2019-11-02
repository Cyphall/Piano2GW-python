import ctypes
import sys

ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "scripts/main.py 0 1 0", None, 1)
