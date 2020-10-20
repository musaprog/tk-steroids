'''
Connecting matplotlib to plot on tkinter canvases.
'''

import numpy as np

import tkinter as tk
import matplotlib.widgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector
import matplotlib.ticker

class CanvasPlotter(tk.Frame):
    '''
    Embedding a matplotlib figure on a tkinter GUI.
    '''
    
    def __init__(self, parent, text='', show=True, visibility_button=False):
        '''
        tk_canvas_master        Tkinter widget to be the master of the created canvas

        '''
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        
        self.frame = tk.LabelFrame(self, text=text)
        self.frame.grid(sticky='NSWE')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)



        self.visibility_button = tk.Button(self.frame, text='', command=self.toggle_visibility)
        
        if visibility_button:
            self.visibility_button.grid(row=0, column=0, sticky='W')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        #self.canvas.get_tk_widget().grid(sticky='NEWS') 
        self.canvas.draw()
        self.show()

        self.roi_callback = None

    def get_figax(self):
        '''
        Returns the figure and ax so that plotting can be done externally.
        Remember to call update method!
        '''
        return self.figure, self.ax

    def plot(self, *args, ax_clear=True, **kwargs):
        '''
        For very simple plotting.
        '''
        if ax_clear:
            self.ax.clear()
        self.ax.plot(*args, **kwargs)
        
        self.canvas.draw()
 
    def __onSelectRectangle(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.roi_callback(x1, y1, x2, y2)
       
    def imshow(self, image, slider=False, roi_callback=None, normalize=True, **kwargs):
        '''
        Showing an image on the canvas, and optional sliders for colour adjustments.
        
        Redrawing image afterwards is quite fast because set_data is used
        instead imshow (matplotlib).

        INPUT ARGUMENTS
        slider          Whether to draw the sliders for setting image cap values
        roi_callback    A callable taking in x1,y1,x2,y2
        *kwargs     go to imshow

        Returns the object returned by matplotlib's axes.imshow.
        '''

        if image is None:
            image = self.imshow_image

        self.imshow_image = image
        
        # Slider
        if slider:
            # Check if the sliders exist. If not, create
            try:
                self.imshow_sliders
            except AttributeError:
                self.slider_axes = [self.figure.add_axes(rect) for rect in ([0.2, 0.05, 0.6, 0.05], [0.2, 0, 0.6, 0.05])]
                
                self.imshow_sliders = []
                self.imshow_sliders.append( matplotlib.widgets.Slider(self.slider_axes[0], 'Upper %', 0, 100, valinit=90, valstep=1) )
                self.imshow_sliders.append( matplotlib.widgets.Slider(self.slider_axes[1], 'Lower %', 0, 100, valinit=5, valstep=1) )
                for slider in self.imshow_sliders:
                    slider.on_changed(lambda slider_val: self.imshow(None, slider=slider, **kwargs))
            
            # Check that the lower slider cannot go above the upper.
            if self.imshow_sliders[0].val < self.imshow_sliders[1].val:
                self.imshow_sliders[0].val = self.imshow_sliders[1].val

            upper_clip = np.percentile(image, self.imshow_sliders[0].val)
            lower_clip = np.percentile(image, self.imshow_sliders[1].val)
            image = np.clip(image, lower_clip, upper_clip)
            
            # Normalize using the known clipping values
            #image = image - lower_clip
            #image = image / upper_clip
        #else:
        # No slider, just normalize from 0 to 1
        if normalize:
            image = image - np.min(image)
            image = image / np.max(image)


        # Just set the data or make an imshow plot
        try:
            self.imshow_obj.set_data(image)
        except AttributeError:
            self.imshow_obj = self.ax.imshow(image, **kwargs)
            self.figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
            self.ax.xaxis.set_major_locator(matplotlib.ticker.NullLocator()) 
            self.ax.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
            if callable(roi_callback):

                if self.roi_callback is None:
                    self.roi_rectangle = RectangleSelector(self.ax, self.__onSelectRectangle, useblit=True)
                
                self.roi_callback = roi_callback
             
        self.canvas.draw()
        
        return self.imshow_obj
    

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
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='NSWE')
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

        self.canvas.get_tk_widget().grid(row=1, column=0, sticky='NSWE')

    def toggle_visibility(self):
        '''
        Toggle wheter the plot is shown or hidden.
        '''

        if self.visible:
            self.hide()
        else:
            self.show()

