'''
Widgets for managing lists of items. 
'''

import tkinter as tk
import tkinter.simpledialog
from tk_steroids.elements import Listbox, ButtonsFrame


class ItemManager(tk.Frame):
    '''
    Adding, removing, renaming items in a list.
    
    Attributes
    ----------
    current : string or None
        Name of the currently selected item (item_name)
    data : dict of dicts
        {item_name: {field1: string1, ...}}
    fields : list of strings
        Names of the fields user can input data (in addition to the
        name of the entry)
    listbox : object
        tk_steroids Listbox (tkinter Listbox object by self.listbox.listbox)
    buttons : object
        tk_steroids ButtonsFrame (self.buttons.buttons for underlying tkinter
        button objects)
    
    selection_callback : callable
        Called when an item is selected
    postchange_callback : callable
        Called after an item is removed, renamed or added
    save_callback : callable
        Callable when pressing save button
    cancel_callback : callable
        Callable when pressing close button
    '''

    def __init__(self, parent, fields=[], start_data={},
            selection_callback=None, postchange_callback=None,
            save_callback=None, cancel_callback=None):
        '''
        parent : object
            Tkinter parent widget
        start_data : dict of dicts OR dict of lists
            Initial entries in form {item_name: {field1: string1, ...}}
            or {item_name: [string1, string2, ...]}
        '''

        tk.Frame.__init__(self, parent)
        
        self.current = None
        self.fields = fields
        self.data = start_data
        self.selection_callback = selection_callback
        self.postchange_callback = postchange_callback
        
        # Left side entries

        self.listbox = Listbox(self, list(self.data.keys()), self._on_listbox_selection)
        self.listbox.grid(row=1, column=1, sticky='NSWE')

        
        # Right side buttons frame
        button_names = ['Add', 'Remove']
        button_commands = [self.add, self.remove]
        
        self.buttons = ButtonsFrame(self, button_names, button_commands, horizontal=False)
        self.buttons.grid(row=1, column=2)
        
        if callable(save_callback):
            tk.Button(self, text='Save', command=save_callback).grid(row=2, column=1)
        if callable(cancel_callback):
            tk.Button(self, text='Cancel', command=cancel_callback).grid(row=2, column=2)
        
        # Specify stretching
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)


    def add(self):
        name = tkinter.simpledialog.askstring('New entry', 'Item name')
        if name:
            self.data[name] = {}

        self.listbox.set_selections(list(self.data.keys()))
        
        if self.postchange_callback:
            self.postchange_callback(self.data)
    

    def remove(self):
        
        del self.data[self.current]
        
        self.listbox.set_selections(list(self.data.keys()))
        
        if self.postchange_callback:
            self.postchange_callback(self.data)
 

    def _on_listbox_selection(self, selection):
        self.current = selection
        
        if self.selection_callback:
            self.selection_callback(self.data[selection])
   

    def set_data(self, data):
        '''
        data : list or dict
            [item1, item2, ...] or {item1: {}, item2: {}}
            where item_i is a string.
        '''
        if isinstance(data, list):
            self.data = {key: {} for key in data}
        else:
            self.data = data
        
        self.listbox.set_selections(list(self.data.keys()))
   


class ListManager(tk.Frame):
    '''
    Like ItemManager but each item is a further sublist.
    See ItemManager for documentation.
    '''
    
    def __init__(self, parent, start_data=[],
            save_callback=None, cancel_callback=None):
        tk.Frame.__init__(self, parent)

        self.im2 = ItemManager(self,
                save_callback=save_callback, cancel_callback=cancel_callback)
        self.im1 = ItemManager(self, start_data=start_data,
                selection_callback=self.im2.set_data)

        self.im2.postchange_callback = self.update_im1

        self.im1.grid(row=1, column=1, sticky='NSWE')
        self.im2.grid(row=1, column=2, sticky='NSWE')

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)


    def update_im1(self, data):
        self.im1.data[self.im1.current] = list(data.keys())
        self.im1.listbox.set_selections(list(self.im1.data.keys()))

