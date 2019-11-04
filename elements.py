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
        in the listbox happens.

        The current selection is passed as the one and only argument to the callback function.
        '''
        
        tk.Frame.__init__(self, parent)
        self.parent = parent
        

        self.listbox = tk.Listbox(self)
        self.listbox.grid(sticky='NS')
       
        self.scrollbar= tk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky='NS')
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)


        self.set_selections(selections)
        
        self.listbox.bind('<<ListboxSelect>>', lambda x: self._errorchecked(callback))
        
        # Make the listbox to stretch in North-South to take all the available space
        self.rowconfigure(0, weight=1)
        #parent.rowconfigure(2, weight=1)


    def _errorchecked(self, callback):
        '''
        
        '''
        try:
            sel = self.listbox.curselection()[0]
            argument = self.selections[sel]
        except:
            argument = None

        if not argument is None:
            callback(self.selections[sel])

    def set_selections(self, selections):
        
        # Empty current as it may have old entries
        self.listbox.delete(0, tk.END)
        
        self.selections = selections
        
        for item in self.selections:
            self.listbox.insert(tk.END, item)



class Tabs(tk.Frame):
    '''
    Tabs widget. Can contain any tkinter widgets.
    '''
    def __init__(self, parent, tab_names, elements):
        '''
        
        *sub_elements   Constructors of the elements that get to initialized,
                        only one argument allowed, the parent
        '''

        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.current = 0

        self.buttons = []
        self.initialized_elements = []

        # Initialize content/elements
        for i_button, (name, element) in enumerate(zip(tab_names, elements)):

            initialized_element = element(self)
            self.initialized_elements.append(initialized_element)
            

            button = tk.Button(self, text=name, command=lambda i_button=i_button: self.button_pressed(i_button))
            button.grid(row=0, column = i_button)
            self.buttons.append(button)
            

        self.initialized_elements[self.current].grid(row=1, columnspan=len(self.buttons))

    def button_pressed(self, i_button):
        print(i_button) 
        self.initialized_elements[self.current].grid_remove()
        self.current = i_button
        
        self.initialized_elements[self.current].grid(row=1, columnspan=len(self.buttons))

    def get_elements(self):
        '''
        Returns the initialized elements which have to the Tab as their master/parent.
        '''
        return self.initialized_elements


class ButtonsFrame(tk.Frame):
    '''
    If you just need a frame with simply buttons (with a callback) next to each other,
    use this widget.
    '''

    def __init__(self, parent, button_names, button_commands):
        '''
        '''
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        self.buttons = []

        for i_button, (name, command) in enumerate(zip(button_names, button_commands)):
            button = tk.Button(self, text=name, command=command)
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
    





def main():
    pass

if __name__ == "__main__":
    main()
