import copy 

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

class TickSelect(tk.Frame):
    '''
    User sets ticks to select items from selections group and
    presses ok -> callback_on_ok gets called as the made selections list
    as the only input argument.
    '''

    def __init__(self, parent, selections, callback_on_ok, close_on_ok=True, ticked=None,
            callback_args=[], callback_kwargs={}):
        '''
        selections          List of strings
        callback_on_ok      Callable, whom a sublist of selections is passed
        close_on_ok         Call root.destroy() when pressing ok
        ticked              A sublist of selections that should be enabled by default.
        callback_args       A list of secondary callback arguments, passed after the selections
        callback_kwargs     A dict of callback keyword arguments
        '''
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1) 
        
        self.callback_on_ok = callback_on_ok
        self.selections = selections
        self.close_on_ok = close_on_ok

        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs

        # Add scrollbar - adds canvas and extra frame
        canvas = tk.Canvas(self)
        frame = tk.Frame(canvas)
        frame.grid(row=0, column=0, sticky='NSEW')

        scrollbar = tk.Scrollbar(self, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='NS')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0,0), window=frame, anchor='nw')
        
        canvas.grid_rowconfigure(0, weight=1)
        canvas.grid(row=0, column=0)
        

        # Create tickboxes and entries
        N_selections = len(self.selections)
        tk_variables = [tk.IntVar() for i in range(N_selections)]

        for i_row, selection in enumerate(self.selections):        
            checkbutton = tk.Checkbutton(frame, text=selection, variable=tk_variables[i_row])
            checkbutton.grid(sticky='W')
            
            # Set ticked
            if not ticked is None and selection in ticked:
                checkbutton.select()

        tk.Button(self, text='Ok', command=self.on_ok).grid(row=1, column=0)
        self.winfo_toplevel().after(50, self._update)
        
        self.frame = frame
        self.canvas = canvas
        self.tk_variables = tk_variables


    def _update(self):
        self.canvas.config(scrollregion=(0, 0, self.frame.winfo_reqwidth(), self.frame.winfo_reqheight()))
        self.winfo_toplevel().after(1000, self._update)


    def on_ok(self):
        '''
        Gets called when the OK button is pressed, and calls callback_on_ok with
        the made selections.
        '''
        made_selections = []

        for tk_variable, selection in zip(self.tk_variables, self.selections):
            if tk_variable.get() == 1:
                made_selections.append(selection)

        
        self.callback_on_ok(made_selections, *self.callback_args, **self.callback_kwargs)
        

        if self.close_on_ok:
            self.winfo_toplevel().destroy()


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
    def __init__(self, parent, tab_names, elements=None,
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

        on_select_callback : callable
            Callback that is executed just before changing the tab.
            Has to take in one argument that is new i_current (integer).
        
        '''

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
        self.pages[self.i_current].grid(row=1, columnspan=len(self.buttons))


    def get_elements(self):
        '''
        Returns the initialized elements which have to the Tab as their master/parent.
        '''
        return self.pages



class ButtonsFrame(tk.Frame):
    '''
    If you just need a frame with simply buttons (with a callback) next to each other,
    use this widget.
    '''

    def __init__(self, parent, button_names, button_commands, title=''):
        '''
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
            button.grid(row=0, column=i_button)
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
