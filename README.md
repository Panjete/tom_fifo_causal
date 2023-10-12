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