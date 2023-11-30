import tkinter as tk
import tkinter.scrolledtext

class Listbox(tk.Frame):
    '''Tkinter's Listbox and Scrollbar wrapped for convienece.
    
    At the init, it takes in a list of selectable options, and a callback function.
    When the user selects and item, it evokes the callback that receives
    the user selection (one of the selectable options) as the input
    (or None if no selection).
    
    Attributes
    ----------
    selections : list of strings
        Items that show up in the listbox
    callback : callable
        The callback function
    parent : object
        Parent widget
    listbox : object
        Tkinter's Listbox widget
    scrollbar : object
        Tkinter's Scrollbar widget
    '''

    def __init__(self, parent, selections, callback, maintain_selected=True):
        '''
        maintain_selected : bool
            If true, clicking other Listboxes or widgets does not make the current
            selection to None (deselecting the selected)
        '''
        
        tk.Frame.__init__(self, parent)
        self.parent = parent

        
        self.maintain_selected = maintain_selected

        self.listbox = tk.Listbox(self, height=20)
        self.listbox.grid(sticky='NSEW')
       
        self.scrollbar= tk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky='NS')
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)


        self.set_selections(selections) # self.selections = selections
        self.callback = callback
        
        self.listbox.bind('<<ListboxSelect>>', self._call_callback)
        
        # Make the listbox to stretch in North-South to take all the available space
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self._previous_selection = None
        self._state_valid = True


    def _call_callback(self, *args):
        '''Validate selection and the callback and call back
        '''
        try:
            sel = self.listbox.curselection()[0]
            argument = self.selections[sel]
            self._previous_selection = argument
            self._state_valid = True
        except:
            argument = None

        if not argument is None and callable(self.callback):
            self.callback(self.selections[sel])



    def set_selections(self, selections, colors=None):
        '''Reset the selectables

        Options
        -------
        selections : list of strings
            
        colors : list
            A list of valid tkinter colors. It sets
            the background color for each selectable in the Listbox.
        '''
        
        # Empty current as it may have old entries
        self.listbox.delete(0, tk.END)
        
        self.selections = selections
        
        for i_item, item in enumerate(self.selections):
            self.listbox.insert(tk.END, item)
            
            if colors:
                self.listbox.itemconfig(i_item, bg=colors[i_item])


    def disable(self):
        '''Makes the listbox's state unselectable
        '''
        self.listbox.configure(state=tk.DISABLED)


    def enable(self):
        '''Makes the listbox's state selectable
        '''
        self.listbox.configure(state=tk.NORMAL)

    
    def get_current(self):
        '''Returns the current selection.

        Returns None if no selection has been made.
        '''
        if not self._state_valid:
            return None

        try:
            sel = self.listbox.curselection()[0]
            return self.selections[sel]
        except:
            return self._previous_selection

    @property
    def current(self):
        '''
        current : string
            The current selection
        '''
        return self.get_current()

    
    @current.setter
    def current(self, value):
        if value is None:
            self._state_valid = False
            return

        if value not in self.selections:
            raise ValueError(f'"{value}" not in the selections {self.selections}')
        index = self.selections.index(value)
        self.listbox.select_set(index)



class TickboxFrame(tk.Frame):
    '''
    A series of tickboxes (Checkbuttons) and getting their True/False values.
    
    Attributes
    ----------
    states : dict
        True/False
    ticked : list
        self.states keys that have True value
    checkbuttons : list
        tk.Checkbutton objects
    '''

    def __init__(self, parent, options, fancynames=None, defaults=None, ncols=3,
            single_select=False,
            callback=None):
        '''
        parent
            Tkinter parent widget
        options : list of strings
            Names of the options
        fancynames : list of strings
            Names to show on the gui
        defaults : list of bools
            Start values, True for ticked and False for unticked
        ncols : int
            Number of columns
        single_select : bool
            If True, use Radiobuttons instead of Checkbuttons to only have
            one active selection at a time.
        callback : callable
            Executed when there's a change in the tickboxes.
            Gets the self.states dict as an input argument.
        '''
         
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self._single_select = single_select 

        if single_select:
            intvar = tk.IntVar()
            self.__states = {option: intvar for option in options}
            self._option_names = options
            try:
                intvar.set(defaults.index(True))
            except:
                intvar.set(0)

        else:
            self.__states = {option: tk.IntVar() for option in options}
        
            if defaults is not None:
                for option, default in zip(options, defaults):
                    self.__states[option].set( int(default) ) 
            

        if fancynames is None:
            fancynames = {option: option for option in options}
        else:
            fancynames = {option: fancyname for option, fancyname in zip(options, fancynames)}
        
        if single_select:
            self.checkbuttons = [tk.Radiobutton(self, text=fancynames[option],
                variable=self.__states[option], command=callback,
                value=i_option) for i_option, option in enumerate(options)]
        else:
            self.checkbuttons = [tk.Checkbutton(self, text=fancynames[option],
                variable=self.__states[option], command=callback) for option in options]


        i_row = 1
        i_col = 1
        for button in self.checkbuttons:
            button.grid(row=i_row, column=i_col)
            
            i_col += 1
            if i_col > ncols:
                i_col = 1
                i_row += 1
    
    @property
    def states(self):
        if self._single_select:
            return {option: int(self.__states[option].get()) == i for i, option in enumerate(self._option_names)}
        else:
            return {option: bool(intvar.get()) for option, intvar in self.__states.items()}

    @states.setter
    def states(self, s):
        
        for option in self.__states.keys():
            value = s.get(option, None)
            if value is not None:
                self.__states[option].set(value)

    @property
    def ticked(self):
        return [s for s, b in self.states.items() if b]



class SliderFrame(tk.Frame):
    '''
    Multiple sliders (similar to TickboxFrame)
    
    Attributes
    ----------
    options : list
        Names of the variables that the sliders control
    labels : list
        Tkinter Label widgets
    sliders : list
        Tkinter Scale widgets
    '''
    def __init__(self, parent, options, fancynames=None, defaults=None, ncols=1,
            ranges=None, default_range=(0,1),
            resolutions=None, default_resolution=0.01):
        '''
        Options
        -------
        parent : object
            Tkinter parent widget
        options : list of strings
            Names of the variables that the sliders control
        fancynames : list of strings, or None
            Optional, "fancy" names that are shown to the user
        defaults : list or None
            Slider default values
        ncols : int
            Reserved, not yet implemented.
        ranges : list of tuples
            Slider specific ranges (min, max) or None for each slider.
        default_range : tuple of numerical values
            Default (min, max) range
        resolutions : list of numerical values
            Slider specific resolutions or None for each slider.
        default_resolution : numerical
            Default slider resolution
        '''
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(1, weight=1)
 
        self.options = options
        self.labels = []
        self.sliders = []

        for i_row, name in enumerate(options):
            
            if fancynames and fancynames[i_row]:
                fancyname = fancynames[i_row]
            else:
                fancyname = name

            label = tk.Label(self, text=fancyname)
            label.grid(row=i_row, column=0)

            if ranges and ranges[i_row]:
                A, B = ranges[i_row]
            else:
                A, B = default_range

            if resolutions and resolutions[i_row]:
                resolution = resolutions[i_row]
            else:
                resolution = default_resolution

            slider = tk.Scale(self, from_=A, to=B, orient=tk.HORIZONTAL,
                    resolution=resolution)
            slider.grid(row=i_row, column=1, sticky='WE')

            if defaults and defaults[i_row]:
                slider.set(defaults[i_row])

            self.labels.append(label)
            self.sliders.append(slider)


    @property
    def states(self):
        '''
        Returns the slider values dictionary.
        Keys are slider names (options) and items are slider values.
        '''
        return {option: slider.get() for option, slider in zip(self.options, self.sliders)}

    
    @states.setter
    def states(self, s):
        for slider, option in zip(self.sliders, self.options):
            value = s.get(option, None)
            if value is not None:
                slider.set(value)




class DropdownList(tk.Frame):
    '''
    A drop-in replacement for TickboxFrame using tkinter's OptionMenu
    (looks just like OptionMenu)

    Attributes
    ----------
    option_menu : object
        Underlying tkinter OptionMenu object
    label : object
        Underlying tkinter Label object (if label was specified at init)
    '''

    def __init__(self, parent, options, fancynames=None, label=None,
            default=None, callback=None, **kwargs):
        
        tk.Frame.__init__(self, parent)
        
        self.__options = options
        
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
   
        # Check fancynames to show
        if fancynames is None:
            fancynames = options
        else:
            if len(fancynames) != len(options):
                raise ValueError('options and fancynames different lengths, {} vs {}'.format(
                    len(fancynames), len(options)))
        
        self._fancynames = fancynames

        self._state = tk.StringVar(self)
        self._state.set(fancynames[0])
        if callback is not None:
            if callable(callback):
                self._state.trace('w', lambda *args: callback())
            else:
                raise ValueError('callback has to be callable or none, now {}'.format(callback))

        self.option_menu = tk.OptionMenu(self, self._state, *fancynames)
        self.option_menu.grid(row=1, column=2, sticky='NSWE')

        if label:
            self.label = tk.Label(self, text=label)
            self.label.grid(row=1, column=1, sticky='NSWE')
    
    @property
    def states(self):
        index = self._fancynames.index(self._state.get())
        current = self.__options[index]
        return {option: current == option for option in self.__options}

    @property
    def ticked(self):
        '''
        Returns a list of one item, the current selection.
        '''
        index = self._fancynames.index(self._state.get())
        return [self.__options[index]]



class Tabs(tk.Frame):
    '''
    Tabs widget. Can contain any tkinter widgets.

    Attributes
    ----------
    i_current : int
        Index of the currently selected tab.
    buttons : list of objects
        List of tk.Button instances.
    pages : list of objects
        A list of Tkinter widgets the tab holds.
    
    '''
    def __init__(self, parent, tab_names,
            elements=None, draw_frame=False,
            on_select_callback=None):
        '''
        Initializing the tabs.
        
        Arguments
        ---------
        parent
            Tkinter parent widget
        tab_names
            Human readable names, shown in the buttons
        elements : None or list of classes
            If None (by default), initializes tk.Frames as tabs.
            You can get these tk.Frames are in pages attribute.

            Can also classes, that get initialized as this Tabs class
            as the sole argument.
        draw_frame : bool
            If True, draw an extra frame to confine the tabs
        on_select_callback : callable
            Callback that is executed just before changing the tab.
            Has to take in one argument that is new i_current (integer).
        
        '''
        
        # Call init from LabelFrame if framing is wanted
        # Not sure if this can cause problems (when inheriting from tk.Frame)
        if draw_frame:
            tk.LabelFrame.__init__(self, parent)
        else:
            tk.Frame.__init__(self, parent)

        self.parent = parent

        self.on_select_callback = on_select_callback

        self.i_current = 0

        self.buttons = []
        self.pages = []


        buttons_frame = tk.Frame(self)
        buttons_frame.grid()

        if elements is None:
            elements = [tk.Frame for i_tab in tab_names]

        # Initialize content/elements
        for i_button, (name, element) in enumerate(zip(tab_names, elements)):

            initialized_element = element(self)
            self.pages.append(initialized_element)
            

            button = tk.Button(buttons_frame, text=name, command=lambda i_button=i_button: self.set_page(i_button))
            button.grid(row=0, column = i_button, sticky='N')
            self.buttons.append(button)
            

        self.pages[self.i_current].grid(row=1, columnspan=len(self.buttons), sticky='NSEW')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    @property
    def tabs(self):
        return self.pages

    def set_page(self, i_page):
        '''
        When button number i_button is pressed.
        '''
        # Update i_current and take i_old for now
        i_old = self.i_current
        self.i_current = i_page

        if self.on_select_callback is not None:
            self.on_select_callback(self.i_current)

        # Remove the previously gridded widget
        self.pages[i_old].grid_remove()

        # Grid the new widget
        self.pages[self.i_current].grid(row=1, columnspan=len(self.buttons), sticky='NSEW')

        # Change button reliefs (pressed)
        self.buttons[i_old].config(relief=tk.RAISED)
        self.buttons[i_page].config(relief=tk.SUNKEN)


    def get_elements(self):
        '''
        Returns the initialized elements which have to the Tab as their master/parent.
        '''
        return self.pages



class ButtonsFrame(tk.Frame):
    '''
    If you just need a frame with simply buttons (with a callback) next to each other,
    use this widget.
    
    Attributes
    ----------
    buttons : list of objects
        Tkinter button objects
    label : object or None
        If label given at init, store the tk.Label object in this attibute
    '''

    def __init__(self, parent, button_names, button_commands,
            title='', label='', horizontal=True):
        '''
        Arguments
        ---------
        horizontal : bool
            If True, grid buttons horizontally. If False, grid vertically.
        title : string
            If set, init using LabelFrame that encloses the buttons and
            use this text (title) as the label.
        label : string
            Alternative or complementary to the title option, just adds a tk.Label
            as the first button (if avoiding the LabelFrame box is desired).
        '''
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        if title:
            target = tk.LabelFrame(self, text=title)
            target.grid()
        else:
            target = self

        if label:
            self.label = tk.Label(self, text=label)
            if horizontal:
                self.label.grid(row=1, column=0)
            else:
                self.label.grid(row=0, column=1)
        else:
            self.label = None

        self.buttons = []

        for i_button, (name, command) in enumerate(zip(button_names, button_commands)):
            button = tk.Button(target, text=name, command=command)
            
            if horizontal:
                button.grid(row=1, column=i_button+1)
            else:
                button.grid(row=i_button+1, column=1)

            self.buttons.append(button)


    def get_buttons(self):
        '''
        Returns the initialized buttons in the order that the buttons_kwargs
        were delivered in the ButtonsFrame constructor.
        '''
        return self.buttons



class BufferShower(tk.Frame):
    '''
    Redirect any string buffer to be printed on this buffer reader.
    Bit like a non-interactive console window.
    '''
    def __init__(self, parent, string_buffer, max_entries=100):
        '''
        string_buffer       Like StringIO, or sys.stdout
        '''
        tk.Frame.__init__(self, parent)

        self.parent = parent    
        self.string_buffer = string_buffer
        self.max_entries = max_entries
        
        self.entries = 0
        self.offset = 0

        self.text = tkinter.scrolledtext.ScrolledText(self)
        self.text.grid()
        
        self.parent.after(20, self.callback)
        
    def callback(self):
        self.string_buffer.seek(self.offset)

        for line in self.string_buffer:

            if self.entries > self.max_entries:
                self.text.delete('1.0','2.0')

            self.text.insert(tk.END, line)
            self.text.yview(tk.END)
            self.entries += 1
        
        self.offset = self.string_buffer.tell()

        self.parent.after(20, self.callback)
    

class ColorExplanation(tk.Frame):
    '''
    If colors were used in the GUI, this widget can be used easily to
    create help texts to explain meaning of the colors.
    '''

    def __init__(self, parent, colors, help_strings):
        tk.Frame.__init__(self, parent)

        for i_row, (color, string) in enumerate(zip(colors, help_strings)):
            tk.Canvas(self, width=30, height=15, bg=color).grid(row=i_row, column=0, sticky='W')
            tk.Label(self, text=string, font=('System', 8)).grid(row=i_row, column=1, sticky='W')
 


def main():
    pass

if __name__ == "__main__":
    main()
