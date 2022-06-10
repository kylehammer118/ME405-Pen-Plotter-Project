# -*- coding: utf-8 -*-
'''
@author: Grant Gabrielson
@author: Kyle Hammer
Task Data File
'''

import micropython
from ulab import numpy as np
from time import ticks_us, ticks_add, ticks_diff
from math import pi, cos, sin

def TaskDataFun(taskName, period, datalen, drawnum, sendFlag, drawFlag, penFlag, th1, th2):
    
    #functions that are used in Newton Raphson
    
    def g(xdes, theta):
        la = 8.5
        r2 = 0.25
        g_th = np.array([[xdes[0] - la*cos(theta[0][0])],[xdes[1] - la*sin(theta[0][0]) + r2 * theta[1][0]]])
        return g_th

    def dg_dtheta(theta):
        la = 8.5
        r2 = 0.25
        dg_dth = np.array([[la*sin(theta[0][0]),0],[-la*cos(theta[0][0]),r2]])
        return dg_dth

    #Newton Raphson function

    def NewtonRaphson(fcn, Jac, guess, thresh):
    #     theta = np.array([guess[0],guess[1]],'f')
        theta = np.array([guess[0],guess[1]])
        e = 1
        while (e > thresh):
            g = fcn(theta)
            e = np.linalg.norm(g)
            inv = np.linalg.inv(Jac(theta))
            theta = theta - np.dot(inv,g)
        return theta
    
    S0_INIT = micropython.const(0)
    
    S1_OPEN = micropython.const(1)

    S2_PROCESS = micropython.const(2)    

    S3_INTERP = micropython.const(3)
    
    S4_NR = micropython.const(4)
    
    S5_SEND = micropython.const(5)
    
    S6_WAIT = micropython.const(6)

    state = S0_INIT
    
    #For timing
    
    start_time = ticks_us()

    next_time = ticks_add(start_time, period)
    
    while True:

        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:    
            
            next_time = ticks_add(next_time, period)

            if state == S0_INIT:
                
                #creates empty list for data processing
                
                data = [ ]
                xdata = [ ]
                ydata = [ ]
                
                state = S1_OPEN
                yield None
            # 
            elif state == S1_OPEN:
                #more code from the initial UI that did not end up getting implemented
#                if triFlag.read():
#                    with open("Triangle.hpgl","r") as pattern_file:
#                        patt = pattern_file.read()
#                        patt_phases = patt.strip(';').split(';')
#                        patt_phases.pop(-1)
#                        for idx, item in enumerate(patt_phases):
#                            if f'{item[0]},{item[1]}' == 'P,D':
#                                temp_str = str(patt_phases[idx])
#                                temp_str = temp_str[2:]
#                                data = temp_str.strip(',').split(',')
#                    state = S2_PROCESS
#                    yield None
#                    
#                elif cirFlag.read():
#                    with open("Circle.hpgl","r") as pattern_file:
#                        patt = pattern_file.read()
#                        patt_phases = patt.strip(';').split(';')
#                        patt_phases.pop(-1)
#                        for idx, item in enumerate(patt_phases):
#                            if f'{item[0]},{item[1]}' == 'P,D':
#                                temp_str = str(patt_phases[idx])
#                                temp_str = temp_str[2:]
#                                data = temp_str.strip(',').split(',')
#                    state = S2_PROCESS
#                    yield None
#                    
#                elif sqFlag.read():
#                    with open("Square.hpgl","r") as pattern_file:
#                        patt = pattern_file.read()
#                        patt_phases = patt.strip(';').split(';')
#                        patt_phases.pop(-1)
#                        for idx, item in enumerate(patt_phases):
#                            if f'{item[0]},{item[1]}' == 'P,D':
#                                temp_str = str(patt_phases[idx])
#                                temp_str = temp_str[2:]
#                                data = temp_str.strip(',').split(',')
#                    state = S2_PROCESS
#                    yield None
                    
                #Opens the drawing from the names file and puts the data into a list
                with open("Crown.hpgl","r") as pattern_file:
                    patt = pattern_file.read()
                    patt_phases = patt.strip(';').split(';')
                    patt_phases.pop(-1)
                    for idx, item in enumerate(patt_phases):
                        if f'{item[0]},{item[1]}' == 'P,D':
                            temp_str = str(patt_phases[idx])
                            temp_str = temp_str[2:]
                            data = temp_str.strip(',').split(',')
                state = S2_PROCESS
                yield None

                    
            elif state == S2_PROCESS:
                #splits data into x and y by checking if it at an even or odd index
                for idx, item in enumerate(data):
                    if (idx % 2) == 0:
                        xdata.append(int(item))
                    else:
                        ydata.append(int(item))
                
                x_max = float(max(xdata))
                y_max = float(max(ydata))
                
                #scales values with respect to the sixe of the board
                
                x_cal = 7.5/x_max * 0.9    # in/unit
                y_cal = 7.5/y_max * 0.9   # in/unit
                
                for idx, item in enumerate(xdata):
                    x_scaled = (item * x_cal) - 3.5
                    xdata[idx] = x_scaled
                    
                for idx, item in enumerate(ydata):
                    y_scaled = (item * y_cal) + 1
                    ydata[idx] = y_scaled
                    
                state = S3_INTERP
                yield None
                
            elif state == S3_INTERP:
                
                #interpolates the x and y data and writes them to a new list
                
                x_list = [ ]
                y_list = [ ]
                
                for i in range(0, len(xdata)-1):
                    x_interp = np.linspace(xdata[i],xdata[i+1], 10)
                    for item in x_interp:
                        x_list.append(item)
                
                for i in range(0, len(ydata)-1):
                    y_interp = np.linspace(ydata[i],ydata[i+1], 10)
                    for item in y_interp:
                        y_list.append(item)
                
                state = S4_NR
                init = 1
                yield None
                
            elif state == S4_NR:
                
                #only runs when it first enters this state to set initial guess value
                
                if init == 1:
                    
                    #length of data lists that is used for convenience later
                    
                    length = len(x_list)
                    
                    datalen.write(length)
                    
                    data1 = [0]*length
                    data2 = [0]*length
                    
                    th_guess = [pi/6, 4*pi]
                    
                    theta_n = np.array([[th_guess[0]],[th_guess[1]]])
                    init = 0
                    i = 0
                    yield None
                else:
                    
                    #execute Newton Raphson
                    
                    if i < length:
                        x_des = [x_list[i],y_list[i]]
                        theta = NewtonRaphson(lambda theta: g(x_des, theta), dg_dtheta, theta_n, 1e-6)
                        data1[i] = theta[0]
                        data2[i] = theta[1]
                        theta_n = theta
                        i += 1
                    else:
                        send_idx = 0
                        state = S5_SEND
                    yield None
                
            elif state == S5_SEND:
                
                #sends the positional data to the motors 1 at a time
                #waits for send flag so it knows when to send more data
                
                if sendFlag.read():
                    drawnum.write(send_idx)
                    
                    if send_idx == 0:
                        sendFlag.write(False)
                        th1.write(data1[0])
                        th2.write(data2[0])
                        penFlag.write(True)
                        send_idx += 1
                        
                    elif send_idx < length:
                        sendFlag.write(False)
                        th1.write(data1[send_idx])
                        th2.write(data2[send_idx])
                        send_idx += 1
                        yield None
                        
                    #this is for the last run, sets pen flag to false    
                        
                    elif send_idx == length:
                        sendFlag.write(False)
                        th1.write(data1[send_idx])
                        th2.write(data2[send_idx])
                        penFlag.write(False)
                        state = S6_WAIT
                        
                    else:
                        yield None
                        
                else:
                    yield None
                
            elif state == S6_WAIT:
                
                #waits for another drawing (if applicable)
                
                if drawFlag.read():
                    drawFlag.write(False)
                    state = S0_INIT
                    yield None
                else:
                    yield None
            
                    
            # Just in case
            else:
                print('something went wrong')
                break
        else:
            yield None
    
    
    