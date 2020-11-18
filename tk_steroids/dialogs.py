import tkinter as tk

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


def main():
    pass

if __name__ == "__main__":
    main()
