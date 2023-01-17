'''
Widgets to let the user manage a program's settings.
'''

import tkinter as tk


from .routines import (
        inspect_booleans,
        inspect_types
        )
from .elements import (
        TickboxFrame,
        SliderFrame,
        Tabs,
        )


class SettingsManager(tk.Frame):
    '''Display user a settings widget

    Allows building GUIs, where the user manages grouped setting
    values that can be controlled by
        - tickboxes (add_tickboxes)
        - sliders (add_sliders)

    Attributes
    ----------
    elements : dict of lists
        The keys are group names and the items are lists that contain
        TickboxFrame and SliderFrame objects (tk_steroids.elements).
    '''

    def __init__(self, parent):
        '''
        Options
        -------
        parent : object
            Tkinter parent widget
        '''

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        self.elements = {}

        self._container = self


    def _add_setting(self, group, element):
        if group not in self.elements:
            self.elements[group] = []
        self.elements[group].append(element)


    def add_tickboxes(self, group, options, **kwargs):
        '''Add tickboxes

        Options
        -------
        group : string
            Name of the group
        **kwargs
            Keyword arguments to TickboxFrame

       
        Returns
        -------
        tickboxes : object
        '''
        tickboxes = TickboxFrame(self._container, options, **kwargs)
        tickboxes.grid(sticky='NSWE')

        self._add_setting(group, tickboxes)

        return tickboxes


    def add_tickboxes_inspect(self, group, function_or_method,
            exclude_keywords=[], **kwargs):
        '''Add tickboxes inspecting the function_or_method.

        Uses tk_steroids's inspect_booleans to find True/False keyword
        arguments of the given function or method.
        
        Options
        -------
        function_or_method : callable
            A callable for live inspection
        exclude_keywords : dict
            Found settings to exclude
        **kwargs
            Keyword arguments to TickboxFrame

        Returns
        -------
        tickboxes : object
            The tk_steroids' TickboxFrame object
        '''
        options, defaults = inspect_booleans(function_or_method, exclude_keywords)
        return self.add_tickboxes(group, options, defaults=defaults, **kwargs)

    
    def add_sliders(self, group, options, **kwargs):
        ''' Add sliders

        Options
        -------
        group : string
            Group name
        options : list
            Names of the variables that the sliders control
        **kwargs
            Keyword arguments to SliderFrame

        Returns
        -------
        sliders : object
            The tk_steroids' SliderFrame object
        '''
        sliders = SliderFrame(self._container, options, **kwargs)
        sliders.grid(sticky='NSWE')

        self._add_setting(group, sliders)

        return sliders

    
    def add_sliders_inspect(self, group, function_or_method,
            exclude_keywords=[], **kwargs):
        '''Add sliders by inspecting the given function_or_method
        
        Options
        -------
        group : string
            Group name
        function_or_method : callable
        exclude_keywords : dict
        **kwargs
            Keyword arguments to SliderFrame

        See add_sliders for documentation.
        '''
        options, defaults = inspect_types((int, float), function_or_method,
                exclude_keywords, exclude_types=bool)
        return self.add_sliders(group, options, defaults=defaults, **kwargs)


    def get_current(self):
        '''Get current settings

        Returns
        -------
        settings : dict
            {group: {option: value, ...}}
        '''
        settings = {}

        for group in self.elements:

            settings[group] = {}
            for element in self.elements[group]:
                settings[group].update(element.states)

        return settings


    def set_current(self, settings):
        '''Set current settings
        
        Options
        -------
        settings : dict
            {group: {option: value, ...}}
        '''
        for group in self.elements:
            for element in self.elements[group]:
                element.states = settings[group]



class PagedSettingsManager(SettingsManager):
    '''Diplay user a settings widget with multiple pages (tabs)
    
    Attributes
    ----------
    tabs : object
        tk_steroids' Tabs object
    '''

    def __init__(self, parent, page_names):
        super().__init__(parent)
        
        self.tabs = Tabs(self, page_names)
        self.tabs.grid(sticky='NSWE')
        
        self._container = self.tabs.pages[0]

    
    @property
    def active_page(self):
        '''Determines the active tab page, in which new widgets are placed.

        Note. Do not confuse with tab selection
        '''
        return self.tabs.buttons[ self.tabs.i_current ].cget('text')

    @active_page.setter
    def active_page(self, page_name):

        page_names = [button.cget('text') for button in self.tabs.buttons]
        self.cotainer = self.tabs.pages[ page_names.index(page_name) ]


