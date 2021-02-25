import tkinter as tk


def popup_tickselect(tk_parent, *args, title='Make selection', **kwargs):
    top = tk.Toplevel(tk_parent)
    top.title(title)
    top.grid_columnconfigure(0, weight=1)
    top.grid_rowconfigure(1, weight=1)
 
    selector = TickSelect(top, *args, **kwargs)
    selector.grid(sticky='NSEW')

    tk.Button(selector, text='Close', command=top.destroy).grid(row=1, column=1)



class TickSelect(tk.Frame):
    '''
    User sets ticks to select items from selections group and
    presses ok -> callback_on_ok gets called as the made selections list
    as the only input argument.
    '''

    def __init__(self, parent, selections, callback_on_ok, close_on_ok=True, ticked=None,
            callback_args=[], callback_kwargs={}, single_select=False, search=10):
        '''
        selections          List of strings
        callback_on_ok      Callable, whom a sublist of selections is passed
        close_on_ok         Call root.destroy() when pressing ok
        ticked              A sublist of selections that should be enabled by default.
        callback_args       A list of secondary callback arguments, passed after the selections
        callback_kwargs     A dict of callback keyword arguments
        single_select       Use Radiobuttons instead Checkbutton, allowing only one item to be selected.
        search : int or bool
            If True, show the seach bar, false hide. If integer, specifies the number
            of selections when to start showing the search bar.
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
        canvas.grid(row=0, column=0, sticky='NSEW')
        
        self.checkbuttons = []

        # Create tickboxes and entries
        if single_select:
            N_selections = 1
        else:
            N_selections = len(self.selections)
        tk_variables = [tk.IntVar() for i in range(N_selections)]

        for i_row, selection in enumerate(self.selections):        
            if single_select:
                checkbutton = tk.Radiobutton(frame, text=selection, variable=tk_variables[0], value=i_row)
            else:
                checkbutton = tk.Checkbutton(frame, text=selection, variable=tk_variables[i_row])
            checkbutton.grid(sticky='W')
            
            # Set ticked
            if not ticked is None and selection in ticked:
                checkbutton.select()

            self.checkbuttons.append(checkbutton)
    
        # Buttons under the selections list
        self.buttons_frame = tk.Frame(self)
        tk.Button(self, text='Ok', command=self.on_ok).grid(row=1, column=1)
        tk.Button(self.buttons_frame, text='Select all', command=self.select_all).grid(row=1, column=0)
        tk.Button(self.buttons_frame, text='Inverse', command=self.toggle_selection).grid(row=1, column=1)
        self.buttons_frame.grid(row=1, column=0)

        if (search is True) or (search is not False and search < len(self.selections)):
            self.last_search = ''
            self.searchtext = tk.StringVar()
            self.searchbox = tk.Entry(self, text='Search', textvariable=self.searchtext)
            self.searchbox.grid(row=2, column=0, sticky='WE')
            self.winfo_toplevel().after(2000, lambda: self._update_search(repeat_after=1000))

        self.winfo_toplevel().after(50, self._update)
        
        self.frame = frame
        self.canvas = canvas
        self.tk_variables = tk_variables
        self.single_select = single_select
        
        self.visible_checkbuttons = self.checkbuttons


    def _update_search(self, repeat_after=None):
        '''
        Check the searchbox input and hide selections that do not match
        the search.
        '''
        key = str(self.searchtext.get())
        if key != self.last_search:
            
            self.visible_checkbuttons  = []

            for checkbutton in self.checkbuttons:
                checkbutton.grid_remove()
                if key in checkbutton.cget('text'):
                    checkbutton.grid()

                    self.visible_checkbuttons.append(checkbutton)

            self.last_search = key

        if repeat_after:
            self.winfo_toplevel().after(repeat_after, lambda r=repeat_after: self._update_search(repeat_after=r))


    def _update(self):
        self.canvas.config(scrollregion=(0, 0, self.frame.winfo_reqwidth(), self.frame.winfo_reqheight()))
        self.winfo_toplevel().after(1000, self._update)


    def select_all(self):
        for checkbutton in self.visible_checkbuttons:
            checkbutton.select()


    def toggle_selection(self):
        for checkbutton in self.visible_checkbuttons:
            checkbutton.toggle()


    def on_ok(self):
        '''
        Gets called when the OK button is pressed, and calls callback_on_ok with
        the made selections.
        '''
        made_selections = []

        if self.single_select:
            made_selections.append(self.selections[self.tk_variables[0].get()])
        else:
            for tk_variable, selection in zip(self.tk_variables, self.selections):
                if tk_variable.get() == 1:
                    made_selections.append(selection)

        self.callback_on_ok(made_selections, *self.callback_args, **self.callback_kwargs)
        

        if self.close_on_ok:
            self.winfo_toplevel().destroy()


def main():
    pass

if __name__ == "__main__":
    main()
