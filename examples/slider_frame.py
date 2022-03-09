'''
A SliderFrame example
'''

import tkinter as tk
from tk_steroids.elements import SliderFrame

# Create the app
app = tk.Tk()
SliderFrame(app, ['slider1', 'slider2', 'slider3'],
        fancynames= ['Slider 1', None, 'Fancy Slider 3'],
        defaults = [None, 12, -2],
        ranges = [None, (9,12), (-100,100)],
        default_range = (0, 69),
        resolutions = [None, 0.1, 10],
        default_resolution = 1).grid(sticky='NSWE')

app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

app.mainloop()
