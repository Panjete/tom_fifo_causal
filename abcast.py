from copy import deepcopy, copy

class vector_clock:
    ## Each vector_clock class object has the following attributes
    ### state -> Dictionary mapping i->messages recieved from i
    ### n     -> total number of nodes
    ### vid   -> id number of this clock (and the node it belongs to)
    def __init__(self, n, id): 
        ## Creating a vector for the id'th clock
        self.state = dict([(key, 0) for key in range(1, n+1)])
        self.n = n
        self.vid = id

    def recieve_message(self, message):
        ## Updates Blindly, assumes node gives instruction after checking
        for num in range(1, self.n+1):
            self.state[num] = max(self.state[num], message[num])
        #self.state[self.vid] += 1

    def send_message(self, zone):
        ## Yields the state for sending
        if zone:
            self.state[self.vid] += 1
        return self.state
    
class node:
    ## Each node has the folling attributes
    ### vc             -> the vector clock for this node
    ### nid            -> node id
    ### nnodes         -> number of nodes in this system
    ### buffered_queue -> queue of (message, sender_nid) currently unacceptable messages
    def __init__(self, n, id): 
        self.vc = vector_clock(n, id)
        self.nid = id
        self.buffered_queue = []
        self.nnodes = n

    def send_message(self, zone):
        return self.vc.send_message(zone)
    
    def compatibility_message(self, message, recieved_from):
        ## Return value 0 => Buffer it, 1 => Accept it, 2 => Drop it
        self_clock = self.vc.state
        #print("Message recieved by node id ", self.nid, " = ", message, " when self state = ", self_clock)
        flag = 0
        for num in range(1, self.nnodes+1):
            if num == recieved_from:
                if message[num] <= self_clock[num]:
                    flag = 2 ## Duplicate => Drop
                    break
                elif message[num] > self_clock[num]+1:
                    flag = 0 ## Future => Needs to be buffered
                    break
                else:
                    flag = 1
            else:
                if message[num] < self_clock[num]:
                    flag = 2 ## Dupli, Drop
                    break
                elif message[num] > self_clock[num]:
                    flag = 0 ## Causality Disturb, Buffer
                    break
                else:
                    flag = 1

        return flag

    def recieve_message(self, message, recieved_from, orig_request):
        ## Check for compatiblity. Accept and order review of queue if acceptable. Buffer/Drop otherwise
        flag = self.compatibility_message(message, recieved_from)
        if flag == 0:
            print("Message to be buffered by node = ", self.nid, "from = ", recieved_from, '\n')
            self.buffered_queue.append((message, recieved_from))
        elif flag == 1:
            print("Message acceptable by node = ", self.nid, "from = ", recieved_from)
            self.vc.recieve_message(message)
            if orig_request:
                self.minimize_queue()
        else:
            print("Message to be dropped by node = ", self.nid, "from = ", recieved_from, '\n')
        return
    
    def review_queue(self):
        ## Does a single pass over the messages. If something becomes acceptable, accepts and moves on
        if(len(self.buffered_queue) == 0):
            return
        qc = []
        for message, recieved_from in self.buffered_queue:
            #print("checking if removable :- ", message, )
            val_val = self.compatibility_message(message, recieved_from)
            if(val_val == 1):
                print("Queue element removable, message, sender = ", message, recieved_from)
                self.recieve_message(message, recieved_from, False) ## Recieve this, and don't review rest of the queue
            else:
                qc.append((message, recieved_from)) 
        self.buffered_queue = qc
        return

    def minimize_queue(self):
        ## Keep removing from queue until none can be
        print("Recently Recieved a message. Checking if queue can be cleared")
        len_q_start = deepcopy(len(self.buffered_queue))
        while(len(self.buffered_queue) > 0):
            len_q_init = deepcopy(len(self.buffered_queue))
            self.review_queue()
            len_q_later = deepcopy(len(self.buffered_queue))
            if(len_q_init == len_q_later):
                break
        print(len_q_start-len(self.buffered_queue) ," number of elements cleared from queue\n")
        return

    
class nodes_collection:
    def __init__(self, n):
        self.nnodes = n
        self.nodes = dict([(i, node(n, i)) for i in range(1, n+1)])

    def transfer_message(self, n_from, n_to, zone):
        message = self.nodes[n_from].send_message(zone)
        self.nodes[n_to].recieve_message(message, n_from)
        return
    
    def start_sending_message_multicast(self, n_from):
        message = deepcopy(self.nodes[n_from].send_message(True))
        return message
    
    def recieve_message_multicast(self, n_from, n_to, message):
        self.nodes[n_to].recieve_message(message, n_from, True)
        return
    
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

class abcast_system:
    def __init__(self, n):
        self.nodes = dict([(i+1, abcast_node()) for i in range(n)])
        self.n_nodes = n

    def emit(self, message,  n_from, ns_to):
        max_local_timestamp = -1
        for reciever in ns_to:
            self.nodes[reciever].local_timestamp += 1
            self.nodes[reciever].r_queue.append((0,self.nodes[reciever].local_timestamp, message)) ## 0 flag depicts undelivered (ud)
            max_local_timestamp = max(max_local_timestamp, self.nodes[reciever].local_timestamp)
        
        for reciever in ns_to:
            self.nodes[reciever].update_r_queue(max_local_timestamp, message)
            self.nodes[reciever].reorder_r_queue()
            self.nodes[reciever].clean_queue()

        return

        

        


