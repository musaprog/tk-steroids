'''
Connecting matplotlib to plot on tkinter canvases.
'''

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CanvasPlotter(tk.Frame):
    '''
    Creates a tkinter canvas etc. for plotting in GUI.
    '''
    def __init__(self, parent, text='', show=True, visibility_button=True):
        '''
        tk_canvas_master        Tkinter widget to be the master of the created canvas

        '''
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        
        self.frame = tk.LabelFrame(self, text=text)
        self.frame.grid()

        self.visibility_button = tk.Button(self.frame, text='', command=self.toggle_visibility)
        
        if visibility_button:
            self.visibility_button.grid(row=0, column=0, sticky='W')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.draw()
        self.show()

    def get_figax(self):
        '''
        Returns the figure and ax so that plotting can be done externally.
        Remember to call update method!
        '''
        return self.figure, self.ax

    def plot(self, data):
        
        self.ax.clear()
        self.ax.plot(data)
        
        self.canvas.draw()
    

    def hide(self):
        '''
        Hide the canvas widget.
        '''
        self.canvas.get_tk_widget().grid_forget()
        self.visible = False
        self.visibility_button.config(text='Show')


    def show(self):
        '''
        Show the cavas widget.
        (Not to be confused with matplotlib's show)
        '''
        self.canvas.get_tk_widget().grid(row=1, column=0)
        self.visible = True
        self.visibility_button.config(text='Hide')
    

    def update(self):
        '''
        Call if any changes has made to the axes.
        '''
        self.canvas.draw()

    def update_size(self):
        '''
        Sets the frame size to match the matplotlib.Figure size.
        '''
        #self.canvas.config(width=800, height=400)
        w, h = self.figure.get_size_inches() * self.figure.dpi
        self.canvas.get_tk_widget().config(width=h, height=w)

        self.canvas.get_tk_widget().grid(row=1, column=0)

    def toggle_visibility(self):
        '''
        Toggle wheter the plot is shown or hidden.
        '''

        if self.visible:
            self.hide()
        else:
            self.show()

