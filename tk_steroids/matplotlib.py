'''
Connecting matplotlib to plot on tkinter canvases.
'''

import numpy as np

import tkinter as tk
import matplotlib.widgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import (
        RectangleSelector,
        PolygonSelector,
        EllipseSelector
        )
import matplotlib.ticker
from mpl_toolkits.mplot3d import proj3d

import collections

import matplotlib.patches


class ArrowSelector:
    '''
    Idea similar to matplotlib's RectangleSelector.
    '''

    def __init__(self, ax, callback, auto_connect=True):
        '''
        ax              Matlab axes intance
        callback        Gets eclick erelease, as in RectangleSelector
        auto_connect    Calls self.connect at initialization
        '''

        self.ax = ax
        self.callback = callback

        self.fig = ax.figure

        self.p0 = None
        self.p1 = None

        self.cid1 = None
        self.cid2 = None
        self.cid3 = None

        self.arrows = []
        
        if auto_connect:
            self.connect()



    def connect(self):
        '''
        Add ArrowSelector to the figure.

        Calls mpl_connect on self.fig.canvas 
        '''
        self.cid1 = self.fig.canvas.mpl_connect('button_press_event', self._on_press)
        self.cid2 = self.fig.canvas.mpl_connect('button_release_event', self._on_release)



    def disconnect(self):
        '''
        Does the opposite of connect, removes the rectangle selector
        from the figure.
        '''
        self.fig.canvas.mpl_disconnect(self.cid1)
        self.fig.canvas.mpl_disconnect(self.cid2)



    def _on_press(self, event):
        '''
        Called when pressing the figure with mouse.
        '''
        if event.inaxes == self.ax:
            self.p0 = (event.xdata, event.ydata)
            print(self.p0)

            # Set up updating the arrow
            self.cid3 = self.fig.canvas.mpl_connect('motion_notify_event', self._update_arrow)

        else:
            self.p0 = None



    def _clear_arrows(self):
        '''
        Remove any existing arrows from the figure
        '''
        if len(self.arrows) > 0:
            for arrow in self.arrows:
                arrow.remove()
            self.arrows = []
       


    def _update_arrow(self, event):
        '''
        Called when dragging the arrow around.
        '''
        if event.inaxes == self.ax:
            
            self._clear_arrows()
            
            # Arrow thickness
            width = 10

            dx = event.xdata - self.p0[0]
            dy = event.ydata - self.p0[1]
            arrow = matplotlib.patches.Arrow(*self.p0, dx, dy, width=width)
            
            # Add arrow to the figure
            self.ax.add_patch(arrow)
            self.arrows.append(arrow)

            self.fig.canvas.draw_idle()
        else:
            pass



    def _on_release(self, event):
        '''
        Called then releasing the mouse press.
        '''

        if self.cid3 is not None:
            self.fig.canvas.mpl_disconnect(self.cid3)
            self.cid3 = None

        if event.inaxes == self.ax and self.p0 is not None:
            self.p1 = (event.xdata, event.ydata)
            print(self.p1)
            
            # To roughly match RectangleSelector behaviour
            p0 = collections.namedtuple('eclick', ['xdata', 'ydata'])(self.p0[0], self.p0[1])
            p1 = collections.namedtuple('eclick', ['xdata', 'ydata'])(self.p1[0], self.p1[1])
            
            self._clear_arrows()

            self.callback(p0, p1)
        else:
            self.p0 = None
            self.p1 = None




class CanvasPlotter(tk.Frame):
    '''
    Embeds a matplotlib figure on a tkinter GUI.

    Attributes
    ----------
    self.figure : object
        Matplotlib Figure object
    self.ax : object
        Matplotlib Axes object
    self.parent : object
        Tkinter parent widget
    self.visibility_button : object
        A tkinter.Buttton to toggle show/hide
    '''
    
    def __init__(self, parent, text='', show=True, visibility_button=False,
            figsize=None,
            **kwargs):
        '''
        Creates a matplotlib figure and an axes objects when created, and then a
        FigureCanvasTkAgg

        ARGUMENTS
        ---------
        parent : object
            Tkinter parent widget
        text : string
            Title of the plot, to be shown in a Label Frame wrapping the plot
        show : bool
            
        projection : string
            See projection keyword argument for matplotlib's Figure.add_subplot
        '''

        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        if figsize:
            self.figure = Figure(figsize=figsize)
        else:
            self.figure = Figure()
        self.ax = self.figure.add_subplot(111, **kwargs)
        
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
        self._previous_shape = None
        self._previous_roi_drawtype = None


    def get_figax(self):
        '''
        Returns the figure and ax so that plotting can be done externally.
        Remember to call update method!
        '''
        return self.figure, self.ax


    def plot(self, *args, ax_clear=True, **kwargs):
        '''
        For very simple plotting.

        Arguments
        ---------
        *args, **kwargs
            Directly passed to matplotlib plot method
        ax_clear : bool
            If True, clear the previous plottings away
        '''
        if ax_clear:
            self.ax.clear()
        self.ax.plot(*args, **kwargs)
        
        self.canvas.draw()


    def __onSelectRectangle(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.roi_callback(x1, y1, x2, y2)
       
    def __onSelectPolygon(self, vertices):
        self.roi_callback(vertices)
        # FIXME
        # requires manual ESC press to start the selection process again

    
    def imshow(self, image, slider=False, normalize=True,
            roi_callback=None, roi_drawtype='box',
            **kwargs):
        '''
        Showing an image on the canvas, and optional sliders for colour adjustments.
        
        Redrawing image afterwards is quite fast because set_data is used
        instead imshow (matplotlib).

        INPUT ARGUMENTS
        slider          Whether to draw the sliders for setting image cap values
        roi_callback    A callable taking in x1,y1,x2,y2
        roi_drawtype    "box", "ellipse" "line" or "polygon"
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
            
            for ax in self.slider_axes:
                if ax.get_visible() == False:
                    ax.set_visible(True)
           
           
            # Normalize using the known clipping values
            #image = image - lower_clip
            #image = image / upper_clip
        else:
            # Hide the sliders if they exist
            if getattr(self, 'imshow_sliders', None):
                for ax in self.slider_axes:
                    if ax.get_visible() == True:
                        ax.set_visible(False)
                        print('axes not visible not')

        if getattr(self, 'imshow_sliders', None):
            # Check that the lower slider cannot go above the upper.
            if self.imshow_sliders[0].val < self.imshow_sliders[1].val:
                self.imshow_sliders[0].val = self.imshow_sliders[1].val

            upper_clip = np.percentile(image, self.imshow_sliders[0].val)
            lower_clip = np.percentile(image, self.imshow_sliders[1].val)
            image = np.clip(image, lower_clip, upper_clip)
 

        if normalize:
            image = image - np.min(image)
            image = image / np.max(image)


        # Just set the data or make an imshow plot
        if self._previous_shape == image.shape and (
                roi_callback is None or roi_drawtype == self._previous_roi_drawtype):
            self.imshow_obj.set_data(image)
        else:
            if hasattr(self, 'imshow_obj'):
                # Fixed here. Without removing the AxesImages object plotting
                # goes increacingly slow every time when visiting this else block
                # Not sure if this is the best fix (does it free all memory) but
                # it seems to work well
                self.imshow_obj.remove()

            self.imshow_obj = self.ax.imshow(image, **kwargs)
            self.figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
            self.ax.xaxis.set_major_locator(matplotlib.ticker.NullLocator()) 
            self.ax.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
            if callable(roi_callback):

                if getattr(self, "roi_rectangle", None):
                    if self._previous_roi_drawtype == 'line':
                        self.roi_rectangle.disconnect()
                    else:
                        self.roi_rectangle.disconnect_events()

                if roi_drawtype == 'box':
                    self.roi_rectangle = RectangleSelector(self.ax, self.__onSelectRectangle,
                        useblit=True)
                elif roi_drawtype == 'ellipse':
                    self.roi_rectangle = EllipseSelector(self.ax, self.__onSelectRectangle,
                            useblit=True)
                elif roi_drawtype == 'line':
                    self.roi_rectangle = ArrowSelector(self.ax, self.__onSelectRectangle)
                elif roi_drawtype == 'polygon':
                    self.roi_rectangle = PolygonSelector(self.ax, self.__onSelectPolygon,
                            useblit=True)
                else:
                    raise ValueError('roi_drawtype either "box", "ellipse", "line", or "polygon", got {}'.format(roi_drawtype))
                
                self.roi_callback = roi_callback
                self._previous_roi_drawtype = roi_drawtype

        self._previous_shape = image.shape
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


class SequenceImshow(tk.Frame):
    '''
    Higher level CanvasPlotter.imshow for many images with a slider
    to select the current image to show.
    
    Attributes
    ----------
    parent : object
        Tkinter parent widget
    images : list of objects
        List of matplotlib imshow plottable objects.
    canvas_plotter : object
        CavasPlotter object
    slider : object
        Tkitner Scale (slider) for selecting the currently shown image.
    '''

    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent)
        
        self.images = []
        self.canvas_plotter = CanvasPlotter(self, *args, **kwargs)
        self.canvas_plotter.grid(row=1, column=1, sticky='NSWE')
        
        self.slider = tk.Scale(self, from_=1, to=1, orient=tk.HORIZONTAL,
                command=self.select_image)
        self.slider.grid(row=2, column=1, sticky='NSWE')
            
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._imshow_kwargs = {}


    def select_image(self, i_image=None):
        '''
        Callback for self.slider.
        '''
        if i_image is None:
            i_image = self.slider.get()

        self.canvas_plotter.imshow(self.images[int(i_image)-1],
                **self._imshow_kwargs)
        self.slider.set(i_image)


    def imshow(self, images, **kwargs):
        '''
        Set a new set of images to be shown and
        update the slider range.
        
        Arguments
        ---------
        kwargs : dict
            Keyword arguments for CanvasPlotter imshow or
            matplotlib's imshow.
        '''
        self.images = images
        self.slider.config(to=len(images))
        
        if kwargs:
            self._imshow_kwargs = kwargs

        self.select_image(1) 


