
import sys
import io

import tkinter as tk
from tk_steroids.elements import BufferShower

oldout = sys.stdout
sys.stdout = io.StringIO()
print('test')
print('test2')
sys.stdout.write('aana')

root = tk.Tk()
buf = io.StringIO()
BufferShower(root, sys.stdout).grid()
root.mainloop()
