# -*- coding: utf-8 -*-
'''
@author: Grant Gabrielson
@author: Kyle Hammer
TMC2208 Class File
'''

from pyb import Pin

class TMC2208:
    
    def __init__(self, ENN_PIN):
    
        self.ENN = Pin(pin = ENN_PIN, mode = Pin.OUT_PP)
    
    
    def enable(self): # This function enables the TMC2208
        
        self.ENN.high()
        
    
    #def output_diagnostics():
        
    #def settings(mode : str) : int
        #if micro_flag == True: