# -*- coding: utf-8 -*-
'''
@author: Grant Gabrielson
@author: Kyle Hammer
Task User File
'''

import time
import pyb, micropython
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep


def TaskUserFun(taskName, period, drawnum, datalen, drawFlag):
    
    S0_INIT = micropython.const(0)
    
#    S1_SELECT = micropython.const(1)
    
    S1_LCD = micropython.const(1)
    
    S2_PROG = micropython.const(2)

    state = S0_INIT
    
#    serport = pyb.USB_VCP()
    
    #sets the timing for the scheduler
    
    start_time = time.ticks_us()

    next_time = time.ticks_add(start_time, period)   
    
    while True:
        current_time = time.ticks_us()
        if time.ticks_diff(current_time, next_time) >= 0:
            next_time = time.ticks_add(next_time, period)
            
            if state == S0_INIT:
                print('Welcome to our program!')
                
                #Initialize the LCD display
                
                I2C_ADDR = 0x27 #Verified this
                totalRows = 2
                totalColumns = 16
                sdaPIN=pyb.Pin(pyb.Pin.cpu.B9)  #for ESP32
                sclPIN=pyb.Pin(pyb.Pin.cpu.B8)
                i2c = SoftI2C(scl=sclPIN, sda=sdaPIN, freq=10000)
                lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
                state = S1_LCD
                
#We were having trouble getting the file selection to work, so we did not end up including it.
#The state below reflects what we had written before running into problems                

#            elif state == S1_SELECT:
#                printUI()
#                if serport.any():
#                    charIn = serport.read(1).decode()
#                    if charIn in {'t','T'}:
#                        print('Triangle Selected')
#                        triFlag.write(True)
#                        state = S3_WAIT
#                        drawFlag.write(True)
#                        yield None
#                        
#                    elif charIn in {'c','C'}:
#                        print('Circle Selected')
#                        cirFlag.write(True)
#                        state = S3_WAIT
#                        drawFlag.write(True)
#                        yield None
#                        
#                    elif charIn in {'s','S'}:
#                        print('Square Selected')
#                        sqFlag.write(True)
#                        state = S3_WAIT
#                        drawFlag.write(True)
#                        yield None
#                        
#                    elif charIn in {'m','M'}:
#                        printFileInstr()
#                        mFlag.write(True)
#                        state = S4_FILE
#                        yield None
#                    else:
#                        print('Invalid input, try again')
#                        yield None
#                else:
#                    yield None
            
            elif state == S1_LCD:
                
                #prints the welcome message for the lcd
                
                lcd.clear()
                lcd.putstr('Welcome, print  in 3')
                time.sleep(1)
                lcd.clear()
                lcd.putstr('Welcome, print  in 2')
                time.sleep(1)
                lcd.clear()
                lcd.putstr('Welcome, print  in 1')
                drawFlag.write(True)
                time.sleep(1)
                lcd.clear()
                state = S2_PROG
                yield None
                
            elif state == S2_PROG:
                
                #creates the progress bar for the lcd as the arm draws
                
                idx = drawnum.read()
                length = datalen.read()
                prognum = int(idx / length * 16)
                for num in range(0, prognum):
                    lcd.putstr('_')
                
                #prints a finishing message when the machine is done drawing
                
                if idx == length:
                        lcd.clear()
                        lcd.putstr('D')
                        sleep(0.3)
                        lcd.putstr('O')
                        sleep(0.3)
                        lcd.putstr('N')
                        sleep(0.3)
                        lcd.putstr('E')
                        sleep(0.3)
                        lcd.clear()
                        sleep(0.3)
                        lcd.putstr('DONE')
                        sleep(0.3)
                        lcd.clear()
                        sleep(0.3)
                        lcd.putstr('DONE')
                        sleep(0.3)
                        lcd.clear()
                        sleep(0.3)
                        lcd.putstr('DONE')
                        lcd.clear()
                yield None
                
            else:
                print('how did I get here?')
                yield None
                
     
#also a part of what we were going to implement for the user input
#
#def printUI():
#    print('Feel free to draw a premade shape, or import your own file!')
#    print('Press T to draw a triangle')
#    print('Press C to draw a circle')
#    print('Press S to draw a square')
#    print('Press M for instructions to import your own drawing file')
#    
#def printFileInstr():
#    print('To print your own drawing, copy an hgpl file to the MCU')
#    print('Name the file "mydrawing.hpgl"')
    print('Once you upload the file, press D to start drawing')