# -*- coding: utf-8 -*-
'''
@author: Grant Gabrielson
@author: Kyle Hammer
Actuator Class File
'''

from pyb import Pin, Timer

class Actuator:
# This class contrains the necessary functions to use our actuator
        def __init__(self, EN_PIN, IN2A_PIN, IN1A_PIN):
        
            # Initialize all pins
            self.EN = Pin(EN_PIN, mode = Pin.OUT_PP, value=1)
            self.IN2A = Pin(IN2A_PIN, mode = Pin.OUT_PP, value=1)
            self.IN1A_Pin = Pin(Pin.cpu.B4, mode = Pin.OUT_PP, value=1)
            
            # Set the timers
            self.timA = Timer(3, period = 3, prescaler = 0)
            self.clk2 = self.timA.channel(2, pin= self.IN2A_Pin, mode = Timer.PWM, pulse_width = 2)
            self.clk1 = self.timA.channel(1, pin= self.IN1A_Pin, mode = Timer.PWM, pulse_width = 2)
            
        def enable(self): # This function enables the Actuator
            self.EN.high()
            print('Actuator Enabled')
        
        def disable(self): # This function disables the Actuator
            self.EN.low()
            print('Actuator Disabled')
            
        def pen_down(self): # This function extends the actuator to put the pen in the down position
            self.IN1A.high()
            self.IN2A.low()
            print('Pen Down')

        def pen_up(self): # This function retracts the actuator to put the pen in the up position
            self.IN2A.high()
            self.IN1A.low()
            print('Pen Up')