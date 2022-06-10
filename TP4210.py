# -*- coding: utf-8 -*-
'''
@author: Grant Gabrielson
@author: Kyle Hammer
TMC4210 Driver Class File
'''

import pyb
from pyb import SPI, Pin


class TMC4210:
    
    def __init__(self, CLK_PIN, nCS1_PIN, nCS2_PIN, SCK_PIN, MOSI_PIN, MISO_PIN):
        
        # Initialize all pins
        self.CLK = pyb.Pin(pin = CLK_PIN, mode = Pin.OUT_PP)
        self.nCS1 = pyb.Pin(pin = nCS1_PIN, mode = Pin.OUT_PP)
        self.nCS2 = pyb.Pin(pin = nCS2_PIN, mode = Pin.OUT_PP)
        self.SCK = pyb.Pin(pin = SCK_PIN, mode = Pin.OUT_PP)
        self.MOSI = Pin(pin = MOSI_PIN, mode = Pin.OUT_PP)
        self.MISO = Pin(pin = MISO_PIN, mode = Pin.OUT_PP)
        self.spi = SPI(2, SPI.CONTROLLER, baudrate=1_000_000, polarity=1, phase=1, crc=None)
        
    def send_recvarm (self, byte_array): # This function is our send & recieve function for the arm
        self.nCS1.low()
        self.spi.send_recv(byte_array)
        self.nCS1.high()
#        for idx,byte in enumerate(ba): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
            
    def send_recvbelt (self, byte_array): # This function is our send & recieve function for the belt
        self.nCS2.low()
        self.spi.send_recv(byte_array)
        self.nCS2.high()
#        for idx,byte in enumerate(ba): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
    def send(self, byte_array): 
        self.nCS1.low()
        self.nCS2.low()
        self.spi.send(byte_array)
        self.nCS1.high()
        self.nCS2.high()
        
    def sendarm(self, byte_array): # This function is our send function for the arm
        self.nCS1.low()
        self.spi.send(byte_array)
        self.nCS1.high()
    
    def sendbelt(self, byte_array): # This function is our send function for the belt
        self.nCS2.low()
        self.spi.send(byte_array)
        self.nCS2.high()
    
#    def set_mode(self, mode): # This function that we didn't end up implementing is to set the mode for the TMC4210. 
#        self.mode = mode
#        
#        print('Please set the mode:\n'
#                      'Press r for ramp mode.\n'
#                      'Press v for velocity mode.\n'
#                      'Press h for hold mode.\n'
#                      'Press s for soft mode.')
#        
#        if (self.ser.any()):
#            char_in = self.ser.read(1).decode()
#            if(char_in == 'r' or char_in == 'R'):
#                mode = ramp_mode
#            elif(char_in == 'v' or char_in == 'V'):
#                mode = velocity_mode
#            elif(char_in == 'h' or char_in == 'H'):
#                mode = hold_mode
#            elif(char_in == 's' or char_in == 'S'):
#                mode = soft_mode
#        
#        if mode == ramp_mode: #Use for position applications
#            pass
#        elif mode == velocity_mode: #Constant velocity applications, target velocity set by the user
#            pass
#        elif mode == hold_mode: #User sets target velocity
#            pass
#        elif mode == soft_mode: #Similar to ramp mode, probably won't use
#            pass
    
    
    #def set_vel(wset : str) : int
    #This function will wait for user input from taskUser and accept the string that is sent over,
    #and unpackage and convert the string into a binary value that can be used by the driver.
    #For setting velocity, the index must be set to 0100 and RW must be set to 0 for write mode.
    
    #if set_vel_flag == True:
        #SPI.send_recv(send, recv=None, *, timeout=5000)
    
    #def set_acc(aset : str) : int
    
    def CALC_PMUL_PDIV(A_MAX, PULSE_DIV, RAMP_DIV): # This function calculates P_MUL and P_DIV based on the entered parameters. 
        P = A_MAX / (128 * (2 ** (RAMP_DIV - PULSE_DIV)))
        for P_MUL in range(128, 255):
            for P_DIV in range(3, 16):
                P_pr = P_MUL / (2**(3+P_DIV))
                q = P_pr / P
                if q > 0.95 and q < 1:
                    #print(P_MUL)
                    #print(P_DIV)
                    #print(q)
                    return P_MUL, P_DIV
                else:
                    pass
    
    
    def set_target_pos(target_pos): # This function sets the target position. 
        pass    
    
    def int_to_byte(self, num, byte_array): # This function converts integers to bytes. 
        self.byte_arrray[1] = num >> 16
        self.byte_arrray[2] = (num >> 8) & 0xFF
        self.byte_arrray[3] = num & 0xFF
        
    def ticks(self, theta): # This function ___.  
        tcks = int(theta * 384 / 2 / 3.1415)
        return tcks
    
    def get_pos_arm(self): # This function gets the position of the arm. 
        x_actual_reg = bytearray([0b00000011, # Read
                                  0b00000000,
                                  0b00000000,
                                  0b00000000])
        
        x_real = TMC4210.send_recvarm(x_actual_reg)
        x_filt = bytearray([0x00, x_real[1], x_real[2], x_real[3]])
        x_int_real = int.from_bytes(x_filt, "big")
        return x_int_real #ticks
    
    def get_pos_belt(self): # This function gets the position of the belt. 
        x_actual_reg = bytearray([0b00000011, # Read
                                  0b00000000,
                                  0b00000000,
                                  0b00000000])
        
        x_real = TMC4210.send_recvbelt(x_actual_reg)
        x_filt = bytearray([0x00, x_real[1], x_real[2], x_real[3]])
        x_int_real = int.from_bytes(x_filt, "big")
        return x_int_real #ticks
    
    def arm_left(self): # This function sets the offset values to compensate for mechanical limitations. 
        V_MIN_arm_L = bytearray([0b00000100, 
                                 0b00000000,
                                 0b00000011,
                                 0b10000000])
    
        V_MAX_arm_L = bytearray([0b00000110, 
                                 0b00000000,
                                 0b00000011,
                                 0b10000000])
    
        A_MAX_arm_L = bytearray([0b00001100, # Write
                                 0b00000000,
                                 0b00000000,
                                 0b00010010])
        TMC4210.sendarm(V_MIN_arm_L)
        TMC4210.sendarm(V_MAX_arm_L)
        TMC4210.sendarm(A_MAX_arm_L)
        
    def arm_right(self): # This function sets the offset values to compensate for mechanical limitations. 
        V_MIN_arm_R = bytearray([0b00000100, 
                                 0b00000000,
                                 0b00000011,
                                 0b10000000])
    
        V_MAX_arm_R = bytearray([0b00000110, 
                                 0b00000000,
                                 0b00000011,
                                 0b10000000])
    
        A_MAX_arm_R = bytearray([0b00001100, # Write
                                 0b00000000,
                                 0b00000000,
                                 0b00010010])
        TMC4210.sendarm(V_MIN_arm_R)
        TMC4210.sendarm(V_MAX_arm_R)
        TMC4210.sendarm(A_MAX_arm_R)
        
        