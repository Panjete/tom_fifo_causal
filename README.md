## File Structure

1. `top.py` - handles flow control. Call the file like : `python top.py <test_filename> <delay_flags>`

2. `abcast.py` - houses the functionality for the two-phase multicast protocol.

3. `vector_clock.py` - functionality for Causal Order Multicast

4. The test cases rigorously analyse and yield the protocol's behaviour, and their respective features are as follows :-

    * `t_unicast.py` - demonstrates unicast-ability between nodes, and displays the order of reciept of messages sent via unicast is as per the delays encountered within the links they were sent through
    ------
    * `t_basic.py` - simulates two nodes, with variable delays between messages sent in either direction. The order of messages passed to the application layer is the same in both the nodes, as are their _committed_ timestamps, thus showing atomicity and total ordering.
    ------
    * `t1.py` - 3 Nodes with only Multicast Traffic. Final Print statements show the order of messages in which they are passed to the delivery queue. Interim messages printed show the timestamp-communication mechanism at work. This is 
    ------
    * `t_uni_multi.py` - Simulation showing communication in which both unicast and multicast operations are performed. The unicast messages are simply delivered to the delivery queue, while the multicast messaages still show total ordering.
    ------
    * `t_multi_uni.py` - 


## Implementation Details

### Class abcast_node
Built to simulate a communicating node. Has the following attributes :-

* local_timestamp - Indicates serial number used for indexing received messages
* r_queue - To store a priority Queue of messages, and dequeue them when deliverable.
* delivered_messages - Represents the order of messages passed to the upper layers
* id - Unique Number per node
* stored_ts - Contains information to avoid race conditions


An abcast_node can perform the following methods to manipulate it's  state :-


* reorder_r_queue(), when an update may potentially require reodering 
* update_r_queue(message, valid_ts), when a message receieves it's commit time, update local time stamp and mark it deliverable 
* clean_queue() - remove and deliver messages at the head of the queue if deliverable
* receive_message(message) - enqueue in r_queue and update local timestamp
* receive_uni(message) - for handling  unicast messages
* return_local_timestamp_message() - for reporting local timestamp to sender


### Class abcast_system

Built to simulate a system of communicating nodes. Has the following attributes :- 

* nodes - Instances of the abcast_node class
* n_nodes - Number of nodes in the system
* global_clock - To study order of events
* event - To handle race conditions


An abcast_system can perform the following methods to communicate within nodes :-

* start_global_clock() - A daemon that runs in the background and maintains the global clock
* transmit(message,  n_from, n_to, rec_delay) - Send Unicast from n_from to n_to
* emit(message,  n_from, ns_to, rec_delays, reply\_delays, commit_delays) :- Send multicast from n_from to all nodes in n_to, and with delays passed as arguments
* schedule_uni(node_num, induced_delay, message) and schedule_action(node_num, action, induced_delay, message, validation_ts)  :- To transmit messages at the delays required.
    