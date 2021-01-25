'''
// /////////////////////////////////////
// Created on 06.09.2015

@author: DORF_RUST
// /////////////////////////////////////
'''

from client_generic import ClientGeneric
from messages.messagetypes import MSG_CURRENT_POSE_CARTESIAN, MSG_CURRENT_POSE_JOINT, MSG_COMMAND_RECEIVED, MSG_COMMAND_EXECUTED, \
                                MSG_COMMAND, MSG_STOP, MSG_STRING, MSG_FLOAT_LIST, \
                                arm_msg_types_str_array,\
    MSG_CURRENT_POSE_CARTESIAN_BASE

from messages.clientstates import STATE_READY, STATE_READY_TO_RECEIVE, STATE_EXECUTING

import struct
import time
import logging

LOG = logging.getLogger('abb_communication.clients.rfl_robot.communication.client_robot')


#===============================================================================
class ClientRobot(ClientGeneric): #former: inherited from Thread
    """ Client Socket: can be either a client for sending or for receiving data
    the type has to be defined when creating the object with either receiver=True or sender=True
    the sender socket is only for sending data, the receiver socket only for receiving data, this cannot be mixed.
    """
    def __init__(self, parent, host, port,  **params):

        ClientGeneric.__init__(self, parent, host, port,  **params)

    #===========================================================================
    def send(self, msg_type, msg = None):
        """ send message according to message id """
        buf = None

        if msg_type == MSG_COMMAND:
            self.send_command(msg)
        elif msg_type == MSG_STOP:
            msg_snd_len = 12
            params = [msg_snd_len, msg_type] + self.get_header()
            buf = struct.pack(self.byteorder + "2Q3I", *params)
        elif msg_type == MSG_STRING:
            msg_snd_len = len(msg) + 12
            params = [msg_snd_len, msg_type] + self.get_header() + [msg]
            buf = struct.pack(self.byteorder + "2Q3I" + str(len(msg)) +  "s", *params)
        elif msg_type == MSG_FLOAT_LIST:
            msg_snd_len = struct.calcsize(str(len(msg)) + "f") + 12 # float array: length of message in bytes: len*4
            params = [msg_snd_len, msg_type] + self.get_header() + msg
            buf = struct.pack(self.byteorder + "2Q3I" + str(len(msg)) +  "f", *params)

        else:
            LOG.error("Message identifier unknown:  %s = %d, message: %s" % (arm_msg_types_str_array[msg_type], msg_type, msg))
            return

        if buf != None:
            self.socket.send(buf)
            LOG.debug("%s: Sent message: %s to server " % (self.parent.identifier, arm_msg_types_str_array[msg_type]))

    #=====================================================================
    def send_command(self, cmd):
        """ puts the send msg on the stack and calls handle_stack """
        try:
            self.parent.lock.acquire()
            self.parent.stack.append(cmd)
            self.handle_stack()
        finally:
            self.parent.lock.release()

    #===========================================================================
    def _send_command(self, cmd):
        """ msg_type = MSG_COMMAND
        [msg_type, msg_counter, timestamp_sec, timestep_nanosec, cmd_type, float1-float10, int_vel, float_duration, int_zone, int_tool, float_arbitrary, int_rob_num, int_wobj]
        """
        LOG.debug("_send_command: cmd=%s", cmd)
        msg_snd_len = struct.calcsize(str(len(cmd)) + "f") + 12
        params = [msg_snd_len, MSG_COMMAND] + self.get_header() + cmd
        LOG.debug("_send_command: params=%s", params)
        buf = struct.pack(self.byteorder + "2Q" + "3I" + "i" + "10f" + "if2if2i", *params)
        self.socket.send(buf)

    #===========================================================================
    def process(self, msg_len, msg_type, raw_msg):
        """ The transmission protocol for messages is 
        [length msg in bytes] [msg identifier] [other bytes which will be read out according to msg identifier] """
        try:
            self.parent.lock.acquire()

            msg = None

            if msg_type == MSG_COMMAND_RECEIVED:
                msg_counter = struct.unpack_from(self.byteorder + "i", raw_msg)[0]
                self.process_msg_cmd_received(msg_counter)
                #self.parent.update_component()
                #self.parent.update()
                return True
            elif msg_type == MSG_COMMAND_EXECUTED:
                msg_counter = struct.unpack_from(self.byteorder + "i", raw_msg)[0]
                self.process_msg_cmd_executed(msg_counter)
                #self.parent.update_component()  # comment out - stefana
                #self.parent.update()
                return True
            elif msg_type == MSG_CURRENT_POSE_CARTESIAN:
                msg = struct.unpack_from(self.byteorder + "40f", raw_msg)
            elif msg_type == MSG_CURRENT_POSE_JOINT:
                msg = struct.unpack_from(self.byteorder + "36f", raw_msg)
            elif msg_type == MSG_CURRENT_POSE_CARTESIAN_BASE:
                msg = struct.unpack_from(self.byteorder + "40f", raw_msg)
            elif msg_type == MSG_STRING:
                msg = raw_msg
            elif msg_type == MSG_FLOAT_LIST:
                msg = struct.unpack_from(self.byteorder + str((msg_len-12)/4) + "f", raw_msg)
            else:
                LOG.error("%s: Message identifier unknown: %d, message: %s" % (self.parent.identifier, msg_type, raw_msg))
                #self.parent.update_component()  # comment out - stefana
                #self.parent.update() # changed stefana
                return False

            self.parent.put_on_rcv_queue(msg_type, msg)
            #self.parent.update()   # comment out - stefana
            return True
        finally:
            self.parent.lock.release()

    #=====================================================================
    def process_msg_cmd_executed(self, cmd_counter=None):
        """ compares the waypoint counter with the received counter to check if command was executed """
        self.set_cmd_counter_from_client(cmd_counter)

        #self.parent.update()  # comment out - stefana

        #print "command exec: ", cmd_counter
        #print "command exec: cmd_exec_counter_from_client", self.get_cmd_counter_from_client()

        if not len(self.parent.stack) and self.get_cmd_counter() == cmd_counter: #if not len(self.parent.stack) and self.get_stack_counter() == -self.stack_size and self.get_waypoint_counter() == msg_counter:
            LOG.info("Socket: self.publish_state(STATE_READY)")
            self.publish_state(STATE_READY)

    #=====================================================================
    def process_msg_cmd_received(self, msg_counter=None):
        """ count waypoints which are sent back by the Actuator and publish according state """
        self.publish_state(STATE_READY_TO_RECEIVE)
        self.set_stack_counter(+1)
        "Parent will tell the sender socket to handle the stack"
        self.parent.handle_stack()

    #===========================================================================
    # stack handling
    #===========================================================================
    #===========================================================================
    def handle_stack(self):
        try:
            self.parent.lock.acquire()

            if len(self.parent.stack) and self.get_stack_counter() == 0 :
                " The actuator is ready to be programmed, and receives first packet from the stack "
                LOG.info("Socket: The actuator needs to accomplish %i step%s in total." % (len(self.parent.stack), "s" if len(self.parent.stack) > 1 else ""))
                for i in range(min(self.stack_size, len(self.parent.stack))):
                    cmd = self.parent.stack.pop(0)
                    self.set_cmd_counter(+1)
                    self.publish_state(STATE_EXECUTING)
                    self._send_command(cmd)
                    self.set_stack_counter(-1)
            elif len(self.parent.stack) and -self.stack_size <= self.get_stack_counter() < 0 :
                " The actuator is currently STATE_EXEC, but ready to receive another packet from the stack "
                LOG.info("Socket: The actuator needs to accomplish %i step%s in total." % (len(self.parent.stack), "s" if len(self.parent.stack) > 1 else ""))
                cmd = self.parent.stack.pop(0)
                self.set_cmd_counter(+1)
                self.publish_state(STATE_EXECUTING)
                self._send_command(cmd)
                self.set_stack_counter(-1)
            else: # len(self.parent.stack) == 0 and self.stack_counter < 0
                " The actuator must still accomplish some commands and return them "
                LOG.info("Socket: The actuator has still %d step%s to accomplish." % (len(self.parent.stack) + self.get_stack_counter() * -1, "s" if len(self.parent.stack) > 1 else ""))
                pass

        finally:
            self.parent.lock.release()

    #=================================================================================
    def set_stack_counter(self, num):
        self.parent.set_stack_counter(num)
    #=================================================================================
    def get_stack_counter(self):
        return self.parent.get_stack_counter()

    #=================================================================================
    def set_cmd_counter_from_client(self, num):
        self.parent.set_cmd_counter_from_client(num)
    #=================================================================================
    def get_cmd_counter_from_client(self):
        return self.parent.get_cmd_counter_from_client()


if __name__ == '__main__':
    client_rcv = ClientRobot(None, host = "192.168.125.1", port = 30005, receiver = True)
    client_rcv.connect_to_server()
    client_rcv.start()
