import unittest

import tkinter as tk

import tk_steroids.menumaker
from tk_steroids.menumaker import MenuMaker


class SimpleMenu(MenuMaker):
    '''
    A simple method addition to the MenuMaker should lead
    to a menu with item labelled "Return none".
    '''

    def return_none(self):
        return None



class TestMenuMaker(unittest.TestCase):


    def setUp(self):
        
        self.menu = tk.Menu()
        self.maker = SimpleMenu('testmenu')

    
    def test_connect_disconnect(self):

        self.maker._connect(self.menu)
        self.maker._disconnect()
        
        # Important to test reconnecting after disconnecting
        self.maker._connect(self.menu)
        self.maker._disconnect()

    
    def test_enable_disable(self):

        self.maker._connect(self.menu)
        
        self.maker._disable()
        self.maker._enable()

        self.maker._disconnect()

  

