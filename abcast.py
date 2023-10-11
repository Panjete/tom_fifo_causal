from copy import deepcopy, copy
import queue
import time
import threading

class abcast_node:
    def __init__(self):
        self.local_timestamp = 0
        self.r_queue =  []
        self.delivered_messages = []
    
    def reorder_r_queue(self):
        self.r_queue.sort(key = lambda x : x[1]) ## sort on the basis of the timestamp
        return 
    
    def update_r_queue(self, max_local_timestamp, message):
        new_queue = []
        for und, ts, ms in  self.r_queue:
            if ms == message:
                new_queue.append((1, max_local_timestamp, message))
            else:
                new_queue.append((und, ts , message))

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
        self.r_queue = []
        return 

    def receive_message(self, message):
        self.local_timestamp += 1
        self.r_queue.append((0,self.local_timestamp, message)) ## 0 flag depicts undelivered (ud)
        return
    
    def return_local_timestamp_message(self):
        cpy = deepcopy(self.local_timestamp)
        return cpy
            
class abcast_system:
    def __init__(self, n):
        self.nodes = dict([(i+1, abcast_node()) for i in range(n)])
        self.n_nodes = n
        self.global_clock = 0

    def schedule_action(self, node_num, action, induced_delay, message, validation_ts):
        #time.sleep(max(1, induced_delay - self.global_clock))
        time.sleep(max(0, induced_delay))
        if action == "send_broadcast":
            self.nodes[node_num].receive_message(message)
            print("Node Number = ", node_num, " recieved broadcast of message =", message, " at t = ", self.global_clock)
            time.sleep(max(0, validation_ts))
            print("Node Number = ", node_num, " sends back local copy of ts = ", self.nodes[node_num].return_local_timestamp_message(), " at t = ", self.global_clock)
            return self.nodes[node_num].return_local_timestamp_message()
            
        elif action == "host_sends_validation":
            self.nodes[node_num].update_r_queue(validation_ts, message)
            self.nodes[node_num].reorder_r_queue()
            self.nodes[node_num].clean_queue()
            print("Node Number = ", node_num, " fully recieves back message  =", message, " at t = ", self.global_clock)
            return 0
            

    def emit(self, message,  n_from, ns_to):
        max_g_timestamp = self.nodes[n_from].local_timestamp
        threads = []
        queues_storing_ts = []
        for reciever in ns_to:
            def combined_function(ans_storage, reciever):
                ttt = self.schedule_action(reciever, "send_broadcast", 2, message, 3)  ## Everything happens after 2, 3 seconds
                ans_storage.put(ttt)
                #print("for rec = ", reciever, " transmitted local ts = ", ttt)
                return ans_storage
            locale_ts_reciept = queue.Queue()
            thread = threading.Thread(target= combined_function, args=(locale_ts_reciept,reciever))
            queues_storing_ts.append(locale_ts_reciept)
            threads.append(thread)

        for thread in threads:
            thread.start()
        print("All communications Started!")
        for thread in threads:
            thread.join()
        for q in queues_storing_ts:
            max_g_timestamp = max(max_g_timestamp, q.get())

        print("All local timestamps recieved!, max found = ", max_g_timestamp)


        threads = []
        for reciever in ns_to:
            def wf(reciever):
                self.schedule_action(reciever, "host_sends_validation", 2, message, max_g_timestamp) ## Everything happens after 2 seconds
            thread = threading.Thread(target= wf, args= (reciever,)) 
            threads.append(thread)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("Successfully Done!")
        return
    
    def start_global_clock(self):
        while True:
            time.sleep(1)  # Update the clock every second
            self.global_clock += 1
            if self.global_clock == 25:
                break

        

        


