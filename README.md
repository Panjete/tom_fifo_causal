## File Structure

1. `top.py` - handles flow control. Call the file like : `python top.py <test_filename> <delay_flags>`

2. `abcast.py` - houses the functionality for the two-phase multicast protocol.

3. `vector_clock.py` - functionality for Causal Order Multicast

4. The test cases rigorously analyse and yield the protocol's behaviour, and their respective features are as follows :-

    * `t1.py` - 3 Nodes with only Multicast Traffic. Final Print statements show the order of messages in which they are passed to the delivery queue. Interim messages printed show the timestamp-communication mechanism at work. This is 
    ------
    * `t2.py` - dslafvjlkpjdfo