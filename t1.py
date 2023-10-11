from abcast import abcast_node, abcast_system

import threading
import time

print("here!")

a = abcast_system(3)

clock_thread = threading.Thread(target=a.start_global_clock)
clock_thread.daemon = True  # Make it a daemon thread so it doesn't block the main program
clock_thread.start()

a.nodes[1].local_timestamp = 0
a.nodes[2].local_timestamp = 1
a.nodes[3].local_timestamp = 3

print("here too!")

a.emit("M1", 1, [1,2,3])
# a.emit("second node sends", 2, [1,2,3])
# a.emit("third node sends", 3, [1,2,3])

print("dv messages 1 = ", a.nodes[1].delivered_messages)
print("dv messages 2 = ", a.nodes[2].delivered_messages)
print("dv messages 3 = ", a.nodes[3].delivered_messages)

clock_thread.join()