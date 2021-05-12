
import inspect


def inspect_booleans(function_or_method, exclude_keywords=[]):
    '''
    Inspect and get boolean default keyword arguments from a live function
    to be used in TickboxFrame.
    
    Arguments
    ---------
    function_or_method : callable
        An callable on which we apply inspect.signature
    exclude_keywords : list of strings
        Keyword arguments to be excluded by their name.

    Returns
    --------
    options, defaults : list
        Keyword argument names (string) and their default values (bool).
        See TickboxFrame for documentation.
    '''
    options = []
    defaults = []

    for name, param in inspect.signature(function_or_method).parameters.items():
        if param.kind.name in ['POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY']:
            if isinstance(param.default, bool) and name not in exclude_keywords:
                options.append(name)
                defaults.append(param.default)


    return options, defaults


def extend_keywords(keyword_source):
    '''
    Function decorator to extend signature about keyword arguments
    of a function using keywords of another function.

    Useful when you have a wrapper function with **kwargs that get
    directly passed to another function, and you want to use inspecting
    on the wrapper function and gain the keyword arguments of the
    inner function as well.

    Example usge:

        @extend_keywords(hidden_function)
        def wrapping_function(x, a=1, **kwargs):
            ...
            in_between_results = hidden_function(things, **kwargs)
            ...
            return something

        # now using inspect.signature on wrapping function contains also
        # the keywords arguments of the inner fucntion
    
    Arguments
    ---------
    keyword_source : callable
        The source function, which's kws are added to the decorated function.
    '''
    def extended(target_function):
        
        target_signature = inspect.signature(target_function)
        target_param_names = [name for name in target_signature.parameters]

        params_to_add = {}
        kwparams_to_add = {} # VAR_KEYWORD has to be the last if present

        # All parameters of the annotated function
        for name, param in target_signature.parameters.items():
            if param.kind.name not in ['VAR_KEYWORD']:
                params_to_add[name] = param
            else:
                kwparams_to_add[name] = param
        
        # Parameters of the extension source function; Only POSITIONAL_OR_KEYWORD
        # arguments are taken and converted into KEYWORD_ONLY arguments
        for name, param in inspect.signature(keyword_source).parameters.items():
            if param.kind.name in ['POSITIONAL_OR_KEYWORD'] and name not in target_param_names:
                params_to_add[name] = param.replace(kind=inspect.Parameter.KEYWORD_ONLY)

        # Make the new signature and set it as the __signature__ attribute
        # that inspection tools seem to respect
        new_signature = target_signature.replace(
                parameters=list({**params_to_add, **kwparams_to_add}.values()))
        
        target_function.__signature__ = new_signature
        
        return target_function
    return extended

