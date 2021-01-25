'''
// /////////////////////////////////////
// Created on 06.09.2015

@author: DORF_RUST
// /////////////////////////////////////
'''


import time
import logging
from threading import Thread, RLock
from Queue import Queue

from client_robot import ClientRobot

from messages.messagetypes import *
from messages.clientstates import *
from messages.dataqueues import *

#import Global.Storage

from abb_communication.useful.gh_useful import gh_component_timer

LOG = logging.getLogger('abb_communication.clients.rfl_robot.communication.client_container')


class ClientContainer(object):
    """ The Client Container contains 2 Clients that can send and receive data:
    SENDER CLIENT: sends any sort of commands to the sockets, e.g.:
                robot: MSG_COMMAND [counter, position, orientation, 3 integer values]
                base: MSG_MOVE_BASE: [float1, float2] = [seconds to move + fwd or - bwd, speed]
                base: MSG_MOVE_BASE_TO_POS: [position, orientation, speed]
    RECEIVER CLIENT: receives values from the sockets, e.g. streamed position values, or if a command is executed:
                robot or base: MSG_CURRENT_POSE_CARTESIAN: [position, orientation]
                robot or base: MSG_COMMAND_EXECUTED
    """

    # =================================================================================
    def __init__(self, identifier, host='127.0.0.1', port_snd=30003, port_rcv=30004, ghenv = None):

        self.host = host
        self.port_snd = port_snd
        self.port_rcv = port_rcv

        self.identifier = identifier
        self.lock = RLock()

        "The counter for the number of waypoints sent to the client, starts with 0 up to endless."
        self.cmd_counter_to_client = 0

        "The counter for the number of commands sent to the robot, reaches from -self.stack_size to 0."
        self.stack_counter = 0

        " array of commands from the operation which need to be sent to the Actuator"
        self.stack = []

        " Maximum of messages that the actuator can evaluate at once. "
        self.stack_size = 3

        " counter of messages from the clients "
        self.msg_counter_from_client = 0
        self.timestamp_sec_from_client = 0
        self.timestamp_nanosec_from_client = 0
        self.cmd_exec_counter_from_client = 0

        self.publish_state(STATE_READY)
        self.running = False

        self.RECEIVE_QUEUES = DataQueues()
        self.SEND_QUEUE = Queue()

        if self.identifier == "ABB":

            self.RECEIVE_QUEUES.append(DataItem(), MSG_CURRENT_POSE_CARTESIAN)
            self.RECEIVE_QUEUES.append(DataItem(), MSG_CURRENT_POSE_JOINT)
            # added for RFL - stefana
            self.RECEIVE_QUEUES.append(DataItem(), MSG_CURRENT_POSE_CARTESIAN_BASE)
            ##########################
            self.client_snd = ClientRobot(self, host = self.host, port = self.port_snd, sender = True)
            self.client_rcv = ClientRobot(self, host = self.host, port = self.port_rcv, receiver = True)

        else:
            LOG.info("WRONG CLIENT IDENTIFIER")

        self.kill_wait_thread_flag = False

        self.ghenv = ghenv


    # =================================================================================
    def get_connection_state(self):
        return True if self.running == True else False

    # =================================================================================
    def update(self):
        # this updates the component in which the server is created
        if self.ghenv:
            gh_component_timer(self.ghenv, self.running, 1) # update component

    # =================================================================================
    def start_receiver(self):
        """ connects one client to the servers and starts the respective threads """

        ok = self.client_rcv.connect_to_server()
        if ok:
            LOG.info("OK CONNECTED")
            self.client_rcv.thread.start() #self.client_rcv.start()  # start reading in a loop
            self.running = True

    # =================================================================================
    def start_sender(self):
        """ connects one client to the servers and starts therespective threads """

        ok = self.client_snd.connect_to_server()
        if ok:
            LOG.info("OK CONNECTED")
            self.client_snd.thread.start() #self.client_rcv.start()  # start reading in a loop
            self.running = True

    # =================================================================================
    def start(self):
        """ connects both clients to the servers and starts their respective threads """

        #self.waypoint_counter = 0
        if self.running == False:
            ok1 = self.client_snd.connect_to_server()
            ok2 = self.client_rcv.connect_to_server()
            if ok1 and ok2:
                LOG.info("OK CONNECTED")
                self.client_snd.thread.start() #self.client_snd.start()  # start sending from send queue
                self.client_rcv.thread.start() #self.client_rcv.start()  # start reading in a loop
                self.running = True

    # =================================================================================
    def close(self):
        """ closes the sockets of both clients """
        #if self.running:
        self.client_rcv.close()
        self.client_snd.close()

        self.running = False

    # =================================================================================
    def get_snd_queue(self):
        return self.SEND_QUEUE

    # =================================================================================
    def get_rcv_queue(self, msg_id):
        return self.RECEIVE_QUEUES.get(msg_id)

    # =================================================================================
    def put_on_snd_queue(self, msg_id, msg):
        self.SEND_QUEUE.put((msg_id, msg))

    # =================================================================================
    def get_from_snd_queue(self):
        msg_id, msg = self.SEND_QUEUE.get(True, 60)
        LOG.debug("GETTING FROM SEND QUEUE: msg_id=%s, msg=%s", msg_id, msg)
        return msg_id, msg

    # =================================================================================
    def put_on_rcv_queue(self, msg_id, msg):
        q = self.get_rcv_queue(msg_id)
        q.put((msg_id, msg))

    # =================================================================================
    def get_from_rcv_queue(self, msg_id):
        q = self.get_rcv_queue(msg_id)
        msg = q.get()
        return msg

    # =================================================================================
    def send(self, msg_id, msg):
        LOG.debug("PUTTING ON SEND QUEUE: msg_id=%s, msg=%s", msg_id, msg)
        self.put_on_snd_queue(msg_id, msg)

    # =================================================================================
    def handle_stack(self):
        "Just used by Robot Client"
        self.client_snd.handle_stack()

    # =================================================================================
    def publish_state(self, state):
        " Called by self.client_snd and self.client_rcv to change the state from "
        self.lock.acquire()
        self.state = state
        self.lock.release()

    # =================================================================================
    def get_state(self):
        self.lock.acquire()
        state = self.state
        self.lock.release()
        return state

    # =================================================================================
    def set_stack_counter(self, num):
        self.lock.acquire()
        self.stack_counter += num
        self.lock.release()

    # =================================================================================
    def get_stack_counter(self):
        self.lock.acquire()
        sc = self.stack_counter
        self.lock.release()
        return sc

    # =================================================================================
    def set_cmd_counter(self, num):
        self.lock.acquire()
        self.cmd_counter_to_client += num
        self.lock.release()

    # =================================================================================
    def get_cmd_counter(self):
        self.lock.acquire()
        mc = self.cmd_counter_to_client
        self.lock.release()
        return mc

    # =================================================================================
    def set_cmd_counter_from_client(self, num):
        self.lock.acquire()
        self.cmd_exec_counter_from_client = num
        self.lock.release()

    # =================================================================================
    def get_cmd_counter_from_client(self):
        self.lock.acquire()
        mc = self.cmd_exec_counter_from_client
        self.lock.release()
        return mc


    # =================================================================================
    ############### kathrin has no timeout - to clarify!!!!!!!!! ##################
    def wait_for_state_ready(self, delay = None):
        time.sleep(0.05)

        timeout = 0
        state = self.state

        #while state != STATE_READY and timeout < 12000:
        while state != STATE_READY:
            state = self.state
            LOG.debug("state inside loop: %d", state)
            time.sleep(0.05)
            timeout += 1

#             if timeout > 1200:
#                 LOG.error("timeout in state loop")
#                 break

            if self.kill_wait_thread_flag == True:
                return False

        if state == STATE_READY:
            if delay:
                time.sleep(delay)
            return True
        else:
            return False


    # =================================================================================
        ############### kathrin has no timeout - to clarify!!!!!!!!! ##################
    def wait_for_state_ready_to_receive(self, delay = None):
        time.sleep(0.05)
        state = self.state

        timeout = 0
        while (state != STATE_READY_TO_RECEIVE and timeout < 12000) or (state == STATE_READY and timeout < 12000):
            time.sleep(0.05)
            state = self.state
            timeout += 1

            if self.kill_wait_thread_flag == True:
                return False

        if state == STATE_READY or state == STATE_READY_TO_RECEIVE:
            if delay:
                time.sleep(delay)
            return True
        else:
            return False


    # =================================================================================
        ############### kathrin has no timeout - to clarify!!!!!!!!! ##################
    def wait_for_state_executing(self, delay = None):
        time.sleep(0.05)
        timeout = 0
        state = self.state
        while state != STATE_EXECUTING and timeout < 12000:
            state = self.state
            #print "state:", state
            time.sleep(0.05)
            timeout += 1

        if state == STATE_EXECUTING:
            if delay:
                time.sleep(delay)
            return True
        else:
            return False
