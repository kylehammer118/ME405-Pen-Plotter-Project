# -*- coding: utf-8 -*-
'''
@author: Grant Gabrielson
@author: Kyle Hammer
Task Motor File
'''

import micropython 
from TP4210 import TMC4210
from TP2208 import TMC2208
from TPactuator import Actuator
from pyb import Pin, Timer
from time import ticks_us, ticks_add, ticks_diff

def TaskMotorFun(taskName, period, penFlag, sendFlag, th1, th2):
    
    #Create states
    
    S0_INIT = micropython.const(0)
    
    S1_ORIGIN = micropython.const(1)
    
    S2_MOVE = micropython.const(2)
    
    S3_DRAW = micropython.const(3)
    
    #Registers
    
    type_reg = bytearray([0b01110011, # Type_version register
                          0b00000000,
                          0b00000000,
                          0b00000000])
    
    init_4210 = bytearray([0b01101000, # en_sd to 1
                           0b00000000,
                           0b00000000,
                           0b00100000])
    
    V_MIN_belt = bytearray([0b00000100, 
                           0b00000000,
                           0b00000000,
                           0b00000010])
    
    V_MAX_belt = bytearray([0b00000110, 
                           0b00000000,
                           0b00000000,
                           0b00000010])
    
    A_MAX_belt = bytearray([0b00001100, # Write
                           0b00000000,
                           0b00000000,
                           0b00000010])
    
    x_actual_reg = bytearray([0b00000011, # Read
                              0b00000000,
                              0b00000000,
                              0b00000000])
    
    v_actual_reg = bytearray([0b00001011, # Read
                              0b00000000,
                              0b00000000,
                              0b00000000])
    
    a_actual_reg = bytearray([0b00001111, # Read
                              0b00000000,
                              0b00000000,
                              0b00000000])
    
    x_target_reg = bytearray([0b00000000, # Write
                              0b00000000,
                              0b00000000,
                              0b00000000])
    
    x_target_belt_0 = bytearray([0b00000000, # Write
                                 0b00000000,
                                 0b00000000,
                                 0b00000000])
    
    x_target_arm_0 = bytearray([0b00000000, # Write, 384 => 1 rotation
                               0b00000000,
                               0b10000000,
                               0b00000000])
    
    v_target_reg = bytearray([0b00001010, # Write
                              0b00000000,
                              0b11111111,
                              0b11111111])
    
    PULSE_DIV_RAMP_DIV = bytearray([0b00011000, # Write
                                    0b00000000,
                                    0b00000000,
                                    0b00000000])
    
    #Pulse and ramp div computation
    
    PULSE_DIV = PULSE_DIV_RAMP_DIV and (0b1111 << 12)
        
    RAMP_DIV = PULSE_DIV_RAMP_DIV and (0b1111 << 8)
    
    P_VALS = TMC4210.CALC_PMUL_PDIV(1, 0, 0)
    
    P_MUL_P_DIV = bytearray([0b00010010, # Write
                             0b00000000,
                             (0xFF & P_VALS[0]),
                             (0x0F & P_VALS[1])])
    
    RAMP_MODE = bytearray([0b00010100, # Write
                           0b00000000,
                           0b00001100,
                           0b00000000])
    
    state = S0_INIT
    
    #set up timing for the project to run from
    
    start_time = ticks_us()
    
    next_time = ticks_add(start_time, period)
    
    while True:
        
        current_time = ticks_us()
        if ticks_diff(current_time, next_time) >= 0:    
            
            next_time = ticks_add(next_time, period)

            if state == S0_INIT:
                
                #initializes timer and driver and actuator objects
                
                tim = Timer(8, period = 3, prescaler = 0)
                clk = tim.channel(2, pin= clk_Pin, mode = Timer.PWM, pulse_width = 2)
                
                P_MUL = 0
                P_DIV = 0
                
                EN1 = Pin(Pin.cpu.C3, mode=Pin.OUT_PP, value=0) 
                EN2 = Pin(Pin.cpu.C2, mode=Pin.OUT_PP, value=0)
                
                drv_obj = TMC4210(Pin.cpu.C7, Pin.cpu.C0, Pin.cpu.C4, Pin.cpu.B13, Pin.cpu.B14, Pin.cpu.B15)
                
                act_obj = Actuator(Pin.cpu.A10, Pin.cpu.B5, Pin.cpu.B4)               
                act_obj.enable()
                
                #sends relevant registers for motor initiation
                
                drv_obj.send_recvarm(type_reg)
                drv_obj.send_recvbelt(type_reg)
                drv_obj.send(init_4210)
                drv_obj.send(PULSE_DIV_RAMP_DIV)
                drv_obj.send(RAMP_MODE)
                drv_obj.send_recvarm(type_reg)
                drv_obj.send_recvbelt(type_reg)
                
                #new for this testing
                drv_obj.send(P_MUL_P_DIV)
                
                #sends the belt values
                
                drv_obj.sendbelt(V_MIN_belt)
                drv_obj.sendbelt(V_MAX_belt)
                drv_obj.sendbelt(A_MAX_belt)
                
                state = S1_ORIGIN
                yield None
                
            elif state == S1_ORIGIN:
                
                #positions the pen at the origin
                
                act_obj.pen_up()
                drv_obj.sendbelt(x_target_belt_0)
                
                x_0 = int.from_bytes(x_target_arm_0, "big")
                x_real = drv_obj.get_pos_arm()
                
                if abs(x_0 - x_real) < 2:
                    if penFlag.read():
                        act_obj.pen_down()
                        state == S2_MOVE
                        yield None
                    else:
                        yield None
                    
                else:
                    if x_real < x_0:
                        drv_obj.arm_right()
                        drv_obj.sendarm(x_target_arm_0)
                        
                    elif x_real > x_0:
                        drv_obj.arm_left()
                        drv_obj.sendarm(x_target_arm_0)
                    else:
                        pass
                yield None
                
            elif state == S2_MOVE:
                #theta values from Newton Raphson
                theta_arm = th1.read()
                theta_belt = th2.read()
                
                #tick integer values from thetas
                ticks_arm = drv_obj.ticks(theta_arm)
                ticks_belt = drv_obj.ticks(theta_belt)
                
                #target values to send to motors
                x_targ_arm = drv_obj.int_to_byte(ticks_arm, x_target_reg)
                x_targ_belt = drv_obj.int_to_byte(ticks_belt, x_target_reg)
                drv_obj.sendbelt(x_targ_belt)
                
                #actual positional values for the arm
                arm_real = drv_obj.get_pos_arm()
                belt_real = drv_obj.get_pos_belt()
                
                if abs(ticks_arm - arm_real) < 2:
                    #checks if the arm position is close to the desired position
                    if abs(ticks_belt - belt_real) < 2:
                        #checks if the belt position is close to the desired position
                        th1.write(0)
                        th2.write(0)
                        state == S3_DRAW
                        act_obj.pen_down()
                        #puts pen down when it moves to the first spot, and starts to draw
                        yield None
                    else:
                        yield None
                    
                else:
                    #these check the direction of the arm motion so it knows
                    #what velocity and acceleration limits to set to compensate
                    #for the mechanical inconsistencies
                    if ticks_arm > arm_real:
                        drv_obj.arm_right()
                        drv_obj.sendarm(x_targ_arm)
                        
                    elif ticks_arm < arm_real:
                        drv_obj.arm_left()
                        drv_obj.sendarm(x_targ_arm)
                        
                yield None
    
            elif state == S3_DRAW:
                
                sendFlag.write(True)
                
                if (th2.read() != 0) or (th1.read() != 0):
                    #checks if a new theta value has been sent
                    
                    theta_arm = th1.read()
                    theta_belt = th2.read()
                    
                    #tick integer values from thetas
                    ticks_arm = drv_obj.ticks(theta_arm)
                    ticks_belt = drv_obj.ticks(theta_belt)
                    
                    #target values to send to motors
                    x_targ_arm = drv_obj.int_to_byte(ticks_arm, x_target_reg)
                    x_targ_belt = drv_obj.int_to_byte(ticks_belt, x_target_reg)
                    drv_obj.sendbelt(x_targ_belt)
                    
                    arm_real = drv_obj.get_pos_arm()
                    belt_real = drv_obj.get_pos_belt()
                    
                    if abs(ticks_arm - arm_real) < 2:
                        if abs(ticks_belt - belt_real) < 2:
                            sendFlag.write(True)
                            th1.write(0)
                            th2.write(0)
                            yield None
                        else:
                            yield None
                        
                    else:
                        if ticks_arm > arm_real:
                            drv_obj.arm_right()
                            drv_obj.sendarm(x_targ_arm)
                            
                        elif ticks_arm < arm_real:
                            drv_obj.arm_left()
                            drv_obj.sendarm(x_targ_arm)
                            
                    yield None
                
                elif penFlag.read() == False:
                    #raises the pen and brings the position back to the origin
                    #when done drawing
                    
                    act_obj.pen_up()
                    state = S1_ORIGIN
                
            else:
                print('something went wrong')
                break
        else:
            yield None