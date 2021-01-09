'''
// ///////////////////////////////////// 
// Created on 06.09.2015

@author: DORF_RUST
// /////////////////////////////////////  
'''

import time
from threading import Lock
import copy

#===============================================================================
class DataQueues():
    """ A container for all DataQueues from the clients.
    
    Usage: 
    in ClientSocket __init__, e.g. self.identifier = client_id, message identifier = MSG_STRING
    global.DATA_QUEUES.append(DataQueue(self.identifier, MSG_STRING))
    in order to get or put something from this queue:
    dQ = global.DATA_QUEUES.get(self.identifier, MSG_STRING)
    dQ.put(data) / data = dQ.get() => have a look into DataQueue for options
    """
    
    def __init__(self):
        self.queues = {}
        "{'Rhino': {MSG_STRING: DataQueue, MSG_FLOAT: DataQueue}, 'UR': {MSG_COMMAND: DataQueue}}"
        self.lock = Lock()
        
    def append(self, dataqueue, *args):
        
        self.lock.acquire()
        
        if len(args) == 2:
            "Option 1: append with identifier, with msg_id: used for receive queues."
            identifier = [i for i in args if type(i) == type(str())][0]
            msg_id = [i for i in args if type(i) == type(int())][0]
            if not identifier in self.queues:
                self.queues.update({identifier:{}})
            
            self.queues[identifier].update({msg_id:dataqueue})
        
        elif len(args) == 1:
            
            if type(args[0]) == type(str()):
                "Option 2: append with identifier, without msg_id: used for send queues."
                identifier = args[0]
                self.queues.update({identifier:dataqueue})
            
            elif type(args[0]) == type(int()):
                "Option 3: append with just msg_id: used for receive queues in Clients."
                msg_id = args[0]
                self.queues.update({msg_id:dataqueue})
            else:
                raise Exception("DataQueues: No arguments given.")
            
        else: # 'identifier' not in params and 'msg_id' in params
            raise Exception("DataQueues: No arguments given.")
        
        self.lock.release()
    
    def get(self, *args):
        
        #print args
        
        self.lock.acquire()
        
        if len(args) == 2:
            identifier = [i for i in args if type(i) == type(str())][0]
            msg_id = [i for i in args if type(i) == type(int())][0]
            self.lock.release()
            return self.queues[identifier][msg_id]
        
        elif len(args) == 1:
            self.lock.release()
            return self.queues[args[0]]
            
        else:
            self.lock.release()
            raise Exception("DataQueues: No args given.")

#===============================================================================
class DataItem(object):
    """This is for storing respectively overwriting a variable at an global access.
    Is like DataQueue with single item"""
    def __init__(self):
        self.data = None
        self.time_stamp = None
        self.lock = Lock()
    
    def put(self, data, time_stamp = None):
        self.lock.acquire()
        if time_stamp != None:
            self.time_stamp = time_stamp
        else:
            self.time_stamp = time.time()
        self.data = data
        self.lock.release()
    
    def get(self, **params):
        time_stamp = params['time_stamp'] if 'time_stamp' in params else False
        if time_stamp:
            return copy.deepcopy(self.data), copy.deepcopy(self.time_stamp)
        else:
            return copy.deepcopy(self.data)
    
#===============================================================================
class DataQueue(object):
    """ General FIFO queue for storing streamed values in a buffer for global access.
    Edit 15.04.2014 Romana: get with time stamp option !"""
    
    def __init__(self, **params):
        
        self.queue = []
        self.maxsize = 10000
        self.lock = Lock()
        
        self.single_item = params['single_item'] if 'single_item' in params else False
        self.force = params['force'] if 'force' in params else False
        
        # time stamps
        self.timestamps = []
    
    def length(self):
        return len(self.queue)
    
    def put(self, data, time_stamp = None, wait = True):
        """ 
        Options:
        If wait: wait until we can put data
        If self.force: force to put the data on the queue, even if it means to throw something off it
        If self.single_item: just have, one, the most current item in the queue
        """
        
        self.lock.acquire()
        
        if not time_stamp:
            time_stamp = time.time()
                                
        if len(self.queue) == 0:
            " The queue is empty, put item on queue"
            self.queue.append(data)
            self.timestamps.append(time_stamp)
            
        elif len(self.queue) < self.maxsize:   
            " The queue is not empty, but is not yet full, put item on queue "
            
            if self.single_item == False:
                self.queue.append(data)
                self.timestamps.append(time_stamp)
            elif self.single_item == True:
                self.queue = [data]
                self.timestamps = [time_stamp]
            else:
                self.lock.release()
                return False
        else:
            " The queue is full, delete one item and put new item on queue "  
            if self.force == True:
                self.queue.pop(0)
                self.timestamps.pop(0)
                self.queue.append(data)
                self.timestamps.append(time_stamp)
            elif wait == True:
                while self.full():
                    time.sleep(0.000001)
                self.queue.append(data)
                self.timestamps.append(time_stamp)
            else:
                self.lock.release()
                return False
    
        self.lock.release()
        return True
    
    def full(self):
        self.lock.acquire()
        r = len(self.queue) == self.maxsize
        self.lock.release()
        return r
    
    def empty(self):
        self.lock.acquire()
        r = bool(len(self.queue))
        self.lock.release()
        return not r 
        
    def get(self, **params):
        """ 
        Options:
        
        1. no options: get an item off the queue, if its empty return None
        2. If wait: wait until there is an item on the queue, return item
        3. If get_all: get all items off the queue, return list
        4. If keep_data: in any options: don't delete the item or items
        """
        
        wait = params['wait'] if 'wait' in params else False
        get_all = params['get_all'] if 'get_all' in params else False
        keep_data = params['keep_data'] if 'keep_data' in params else False
        time_stamp = params['time_stamp'] if 'time_stamp' in params else False
        
        self.lock.acquire()
        
        if len(self.queue):
            if get_all:
                if keep_data:
                    data = self.queue[:]
                    ts = self.timestamps[:]
                else:
                    data = self.queue[:]
                    ts = self.timestamps[:]
                    self.timestamps = []
                    self.queue = []
            else:
                if keep_data:
                    data = self.queue[0]
                    ts = self.timestamps[0]
                else:
                    data = self.queue.pop(0)
                    ts = self.timestamps.pop(0)
        else:
            if wait == True:
                self.lock.release()
                "Wait until there is something on the queue"
                while not len(self.queue):
                    time.sleep(0.000001)
                self.lock.acquire()
                
                if get_all:
                    if keep_data:
                        data = self.queue[:]
                        ts = self.timestamps[:]
                    else:
                        data = self.queue[:]
                        ts = self.timestamps[:]
                        self.queue = []
                        self.timestamps = []
                else:
                    try:
                        if keep_data:
                            data = self.queue[0]
                            ts = self.timestamps[0]
                        else:
                            data = self.queue.pop(0)
                            ts = self.timestamps.pop(0)
                    except IndexError:
                        data, ts = None, None
            else:
                data = None
                ts = None
                
        self.lock.release()
        
        if time_stamp:
            return data, ts  
        else:  
            return data

#===============================================================================

if __name__ == "__main__":
    

    dQ = DataQueues()
    d = DataQueue()
    dQ.append(d, 1, "Rhino")
    dQ.append(d, 2, "Rhino")
    dQ.append(d, 1, "UR")
    dQ.append(d, 2, "UR")
    #print dQ.get(1, "Rhino")
    print dQ.queues
    
    test_queue = DataQueue()
    dQ.append(test_queue, "TASK_CMDS_FROM_BASE")
    
    test_queue.put([3,[1,1,1,1,1,1,1]])
    test_queue.put([2,2,2,2,2,2,2])
    
    q = dQ.get("TASK_CMDS_FROM_BASE")
    print q
    
    print q.get()
    print q.get()
    print q.get()
    print q.get()

    