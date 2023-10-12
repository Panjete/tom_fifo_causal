from copy import deepcopy, copy
import queue
import time
import threading

class abcast_node:
    def __init__(self, nid):
        self.local_timestamp = 0
        self.r_queue =  []
        self.delivered_messages = []
        self.id = nid
        self.stored_ts  = {}
    
    def reorder_r_queue(self):
        self.r_queue.sort(key = lambda x : x[1]) ## sort on the basis of the timestamp
        return 
    
    def update_r_queue(self, max_local_timestamp, message):
        new_queue = []
        for und, ts, ms in  self.r_queue:
            if ms == message:
                new_queue.append((1, max_local_timestamp, message))
            else:
                new_queue.append((und, ts , ms))

        self.r_queue = new_queue
        return
    
    def clean_queue(self):
        for i in range(len(self.r_queue)):
            und, ts, ms = self.r_queue[i]
            if und == 0:
                self.r_queue = self.r_queue[i:]
                return
            else:
                self.delivered_messages.append((ts,ms))
                #print(self.id, " accepts Message = ", ms)
        self.r_queue = []
        return 

    def receive_message(self, message):
        self.local_timestamp += 1
        self.r_queue.append((0,deepcopy(self.local_timestamp), message)) ## 0 flag depicts undelivered (ud)
        self.stored_ts[message] = deepcopy(self.local_timestamp)
        return
    
    def return_local_timestamp_message(self, message):
        #cpy = deepcopy(self.local_timestamp)
        return self.stored_ts[message] 
    
    def return_and_del_local_tsm(self, message):
        #cpy = deepcopy(self.local_timestamp)
        cpy = self.stored_ts.pop(message, self.local_timestamp)
        return cpy
    
    def receive_uni(self, message):
        self.local_timestamp += 1
        self.delivered_messages.append((deepcopy(self.local_timestamp), message))
        return
    
            
class abcast_system:
    def __init__(self, n):
        self.nodes = dict([(i+1, abcast_node(i+1)) for i in range(n)])
        self.n_nodes = n
        self.global_clock = 0
        self.event = threading.Event()

    def schedule_action(self, node_num, action, induced_delay, message, validation_ts):
        ## Has two modes - rec_broadcast, when it sends message and retrieves local timestamps back
        ##               - host_sends_validation, when the hosts return the commit time and the queues are processed

        #time.sleep(max(1, induced_delay - self.global_clock))
        time.sleep(max(0, induced_delay))
        if action == "rec_broadcast":
            self.nodes[node_num].receive_message(message)
            print("Node Number = ", node_num, " recieved broadcast of message =", message, " at t = ", self.global_clock)
            time.sleep(max(0, validation_ts))
            print("Node Number = ", node_num, " sends back local copy of ts = ", self.nodes[node_num].return_local_timestamp_message(message), " at t = ", self.global_clock)
            return self.nodes[node_num].return_and_del_local_tsm(message)
            
        elif action == "host_sends_validation":
            print("for node == ", node_num, " at t= ", self.global_clock, " init queue = ", deepcopy(self.nodes[node_num].r_queue))
            self.nodes[node_num].update_r_queue(validation_ts, message)
            self.nodes[node_num].reorder_r_queue()
            self.nodes[node_num].clean_queue()
            print("for node == ", node_num, " at t= ", self.global_clock, " queue after valid_msg_rcpt = ", deepcopy(self.nodes[node_num].r_queue))
            print("Node Number = ", node_num, " fully recieves back message  =", message, " at t = ", self.global_clock)
            return 0
        
    def schedule_uni(self, node_num, induced_delay, message):
        ## Has rec_unicast, when it sends message one-way
        time.sleep(max(0, induced_delay))
        self.nodes[node_num].receive_uni(message)
        print("Node Number = ", node_num, " recieved unicast of message =", message, " at t = ", self.global_clock)
        return 
            
    def emit(self, message,  n_from, ns_to, rec_delays, reply_delays, commit_delays):
        ## Does the full broadcast and per-node queue updation
        ## message - the string being shared itself
        ## n_from - the node which shares
        ## ns_to  - nodes being shared to
        ## rec_delays - defines delays sender -> initial reciept
        ## reply_delays - defines delays in rec -> sender ts relay
        ## commit_delays - defines sender -> commit time delays
        max_g_timestamp = deepcopy(self.nodes[n_from].local_timestamp)
        threads = []
        queues_storing_ts = []


        for index, reciever in enumerate(ns_to):
            def combined_function(ans_storage, reciever, del1, del2):
                ttt = self.schedule_action(reciever, "rec_broadcast", del1, message, del2) ## defined link delays
                ans_storage.put(ttt)
                print("For Node = ", reciever,"Local timestamp for M = ", message, " set to ", ttt)
                return ans_storage
            locale_ts_reciept = queue.Queue()
            thread = threading.Thread(target= combined_function, args=(locale_ts_reciept,reciever, rec_delays[index], reply_delays[index]))
            queues_storing_ts.append(locale_ts_reciept)
            threads.append(thread)

        for thread in threads:
            thread.start()
        #print("All communications Started!")
        # for thread in threads:
        #     thread.join()
        for q in queues_storing_ts:
            max_g_timestamp = max(max_g_timestamp, q.get())

        print("All local timestamps recieved!, max found = ", max_g_timestamp)
        # code exits this point only when all q.gets() have been successfull

        threads_v = []
        for index, reciever in enumerate(ns_to):
            def wf(reciever, cdi, mgt):
                self.schedule_action(reciever, "host_sends_validation", cdi , message, mgt) ## Everything happens after 2 seconds
            thread = threading.Thread(target= wf, args= (reciever,commit_delays[index], max_g_timestamp)) 
            threads_v.append(thread)

        for thread in threads_v:
            thread.start()
        for thread in threads_v:
            thread.join()
        #print("Successfully Done!")
        return
    
    def transmit(self, message,  n_from, n_to, rec_delay):
        ## Does the unicast and per-node queue updation
        ## message - the string being shared itself
        ## n_from - the node which shares
        ## n_to  - node being shared to
        ## rec_delay - defines delay sender -> reciept

        def combined_function(reciever, del1, message):
            ttt = self.schedule_uni(reciever, del1, message) ## defined link delays
            return
        thread = threading.Thread(target= combined_function, args=(n_to, rec_delay, message)) 
        thread.start()
        thread.join()
        return
    
    def start_global_clock(self):
        while True:
            time.sleep(1)  # Update the clock every second
            self.global_clock += 1
            self.event.set()
            self.event.clear()
            if self.global_clock == 20:
                break

        

        


