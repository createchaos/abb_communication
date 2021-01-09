'''
// ///////////////////////////////////// 
// Created on 06.09.2015

@author: DORF_RUST
// /////////////////////////////////////  
'''

" Robot States: "
STATE_READY = 1 # the buffer of the robot is empty, he is ready to receive commands (number = stacksize)
STATE_EXECUTING = 2 # the robot is executing the command
STATE_READY_TO_RECEIVE = 3 # the buffer of the robot has space, he is ready to receive the next command
STATE_COMMAND_EXECUTED = 6

STATE_SCANNING = 7 # the base is in scanning mode, when scan is finished, movement can be stopped, now data needs to be processed

" Client States: "
READY = 4
BUSY = 5

client_states_str_array = ["0","STATE_READY","STATE_EXECUTING","STATE_READY_TO_RECEIVE","READY","BUSY", \
                           "STATE_COMMAND_EXECUTED", "STATE_SCANNING"]