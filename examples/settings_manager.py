
import tkinter as tk

from tk_steroids.settings import SettingsManager


def test_function(a, test_function_key1=False,
        test_function_key2=True,
        this_is_not_shown=1,
        this_not_also='test'):
    pass

app = tk.Tk()

sm = SettingsManager(app)
sm.add_tickboxes('Tickables', ['A', 'B', 'C'])
sm.add_tickboxes_inspect('Inspection', test_function)
sm.add_sliders('Slidables', ['x', 'y', 'z'])

sm.grid(sticky='NSWE')

def print_status():
    print( sm.get_current() )

tk.Button(app, text='Print status', command=print_status).grid()

app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)
app.mainloop()
