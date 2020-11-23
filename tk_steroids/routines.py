
import inspect


def inspect_booleans(function_or_method, exclude_keywords=[]):
    '''
    Ispect and get boolean default keyword arguments from a live function
    to be used in TickboxFrame.
    
    Arguments
    ---------
    function_or_method : callable
        An callable on which we apply inspect.getfullargspec
    exclude_keywords : list or srings
        If you want to exclude certain keywords arguments by their name.

    Returns
    --------
    options, defaults : list
        See TickboxFrame for documentation.

    '''
    func_insp = inspect.getfullargspec(function_or_method)
   

    N_args = len(func_insp.args)
    N_defaults = len(func_insp.defaults)
    

    options = []
    defaults = []
    for i in range(N_args-N_defaults, N_args):
        arg = func_insp.args[i]
        default = func_insp.defaults[i-(N_args-N_defaults)]
        if isinstance(default, bool) and arg not in exclude_keywords:
            options.append(arg)
            defaults.append(default)    
    
    return options, defaults

