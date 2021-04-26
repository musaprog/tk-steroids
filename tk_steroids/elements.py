import tkinter as tk
import tkinter.scrolledtext

class Listbox(tk.Frame):
    '''
    Essentially tkinter's Listbox rewrapped.
    
    At initialization, a list of selectable options are passed together with a callback
    function, which on selection is called using the current selection as the input
    argument.
    '''

    def __init__(self, parent, selections, callback):
        '''
        SELECTIONS
        A list of strings that make up the listbox. The selection is passed
        to the callback function.
        
        CALLBACK
        Set the callback function that is called when any change or selection
        in the listbox happens. The only argument that the callback function gets
        is the selection (as shown) or None if no selection or error happens.

        The current selection is passed as the one and only argument to the callback function.
        '''
        
        tk.Frame.__init__(self, parent)
        self.parent = parent
        

        self.listbox = tk.Listbox(self, height=20)
        self.listbox.grid(sticky='NSEW')
       
        self.scrollbar= tk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky='NS')
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)


        self.set_selections(selections)
        
        self.listbox.bind('<<ListboxSelect>>', lambda x: self._errorchecked(callback))
        
        # Make the listbox to stretch in North-South to take all the available space
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)



    def _errorchecked(self, callback):
        '''
        Does some error checking related to the selection(?)        
        '''
        try:
            sel = self.listbox.curselection()[0]
            argument = self.selections[sel]
        except:
            argument = None

        if not argument is None:
            callback(self.selections[sel])

    def set_selections(self, selections, colors=None):
        '''
        Allows resetting the selections.

        colors          A list of valid tkinter colors, one for each selection
        '''
        
        # Empty current as it may have old entries
        self.listbox.delete(0, tk.END)
        
        self.selections = selections
        
        for i_item, item in enumerate(self.selections):
            self.listbox.insert(tk.END, item)
            
            if colors:
                self.listbox.itemconfig(i_item, bg=colors[i_item])


    def disable(self):
        self.listbox.configure(state=tk.DISABLED)


    def enable(self):
        self.listbox.configure(state=tk.NORMAL)

    
    def get_current(self):
        try:
            sel = self.listbox.curselection()[0]
            return self.selections[sel]
        except:
            return None



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

    @property
    def ticked(self):
        return [s for s, b in self.states.items() if b]


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
    '''

    def __init__(self, parent, button_names, button_commands,
            title='', horizontal=True):
        '''
        Arguments
        ---------
        horizontal : bool
            If True, grid buttons horizontally. If False, grid vertically.
        '''
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        if title:
            target = tk.LabelFrame(self, text=title)
            target.grid()
        else:
            target = self

        self.buttons = []

        for i_button, (name, command) in enumerate(zip(button_names, button_commands)):
            button = tk.Button(target, text=name, command=command)
            
            if horizontal:
                button.grid(row=0, column=i_button)
            else:
                button.grid(row=i_button, column=0)

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
