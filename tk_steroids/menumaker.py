
import tkinter as tk


class MenuMaker:
    '''
    An alternative way to make an tkinter menu structures, with an aim to
    improve code readability.


    Intended usage

        1) Create a new class inheriting from MenuMaker class
        2) Add new methods. These become the menu items (see the NOTE1)
        3) Create an object and call _connect(tk_parent_menu)

        NOTE1: About method naming:
            - Method names starting with underscore are excluded from the menu
                (all the original methods start with an unserscore)
            - Menu items are named after the method names
            - Method "use_underscore_names" would become "Use underscore names"
            - Mofidy replacement_dict attribute if you want to change this


    To overload the alphabetical ordering, modify
        _force_order


    (Private) attributes
    ------------------
    self.name
        Name of the menu
    self.replacement_dict
        A dictionary. Keys are strings in method names to be replaced by
        the values. Default is {'_': ' '}
    self.tkmenu
        None when not connected, otherwise a tkinter.Menu object
    self.added_menu_items
        A list of menu item names added to the menu (labels, string)
        For separators, index of the separator when added
    
    '''


    def __init__(self, name):
        '''
        name        Name of the menu as shown on screen.
        '''
        
        self.name = name
        self.replacement_dict = {'_': ' '}

        self.parent_menu = None
        self.tkmenu = None
        self.added_menu_items = []
        
        

    def _connect(self, tk_parent_menu, **kwargs):
        '''
        Create a new menu, populate it with the commands, and
        connect the menu to the tkmenu.

        **kwargs are passed to the created menu.
        '''

        self.parent_menu = tk_parent_menu
        self.tkmenu = tk.Menu(tk_parent_menu, **kwargs)

        method_names = self._force_order()
        
        all_method_names = self._list_items(fancy_names=False)
        
        if method_names is None:
            # In case self._force_order not overridden just use alphabetical
            # listing of all method names
            method_names = all_method_names
        else:
            # Make sure to add also those methods that were
            # not speified in self._force_order
            method_names += [name for name in all_method_names if name not in method_names]


        for method_name in method_names:
            
            if method_name == '.':
                
                self.tkmenu.add_separator()

                index = self.tkmenu.index(tk.END)
                self.added_menu_items.append(index)

            else:
                method = getattr(self, method_name)
                fancyname = self._fancy_name(method_name)

                self.tkmenu.add_command(label=fancyname, command=method)
                
                self.added_menu_items.append(fancyname)
        
        self.parent_menu.add_cascade(label=self.name, menu=self.tkmenu)



    def _disconnect(self):
        '''
        Remove menu items added by this menumaker from the menu.
        '''
        
        if self.tkmenu is None:
            raise ValueError("MenuMaker not connected to a tkinter.Menu object; Cannot disconnect.")


        for item in self.added_menu_items:
            self.tkmenu.delete(item)

        self.parent_menu.delete(self.name)

        self.parent_menu = None
        self.tkmenu = None
        self.added_menu_items = []



    def _fancy_name(self, name):
        '''
        Make a method name into a fancy name.
        
        By default, underscores are replaced by spaces and the name
        is capitalized.
        '''
        fancyname = name[0].upper() + name[1:]

        for original, replacement in self.replacement_dict.items():
            fancyname = fancyname.replace(original, replacement)
        
        return fancyname



    def _list_items(self, fancy_names=False):
        '''
        Returns a list of menu item names (in alphabetical order).

        If fancy_names == True,
        returns the method names as they are shown in the menu.
        '''

        method_names = [method for method in dir(self)
                if not method.startswith('_') and callable(getattr(self, method))]
        method_names.sort()
        
        if fancy_names:
            method_names = [self._fancy_name(name) for name in method_names]

        return method_names
        


    def _enable(self):
        '''
        Enable (make clickable) the menu entries added by this menumaker.
        '''

        if self.tkmenu is None:
            raise ValueError("MenuMaker not connected to a tkinter.Menu object; Cannot enable items.")
        
        raise NotImplementedError('Enabling not implemented yet')



    def _disable(self):
        '''
        Disable (make unclickable) the menu entries added by this menumaker.
        '''
        if self.tkmenu is None:
            raise ValueError("MenuMaker not connected to a tkinter.Menu object; Cannot disable items.")
        
        raise NotImplementedError('Disabling not implemented yet')



    def _force_order(self):
        '''
        Override this method to force order by returning an interable of the
        methods (menu item) names (you can get the list of all names using _list_items)
        
        '.' represents a menu separator.

        For example, return ['open_window', 'close_some_window', '.', 'exit']
        to have separator in between "Close some window" and "Exit"

        '''
        return None


