from abcast import abcast_node, abcast_system
import threading

a = abcast_system(3)

clock_thread = threading.Thread(target=a.start_global_clock) ## global clock
clock_thread.daemon = True  # Making it a daemon thread so that it doesn't block the main program
clock_thread.start()

## Setting random time-delays and unicast communication
thread1 = threading.Thread(target= (lambda: a.transmit("M_uni 5", 3, 1, 12))) 
thread2 = threading.Thread(target= (lambda: a.emit("M1", 1, [1,2,3], [4, 4, 2], [3, 3, 3], [0, 0, 0])))
thread3 = threading.Thread(target= (lambda: a.transmit("M_uni 1", 1, 2, 0)))  
thread4 = threading.Thread(target= (lambda: a.transmit("M_uni 2", 2, 3, 4))) 
thread5 = threading.Thread(target= (lambda: a.emit("M2", 2, [1,2,3], [6, 2, 6], [5, 5, 5], [0, 0, 0]))) 
thread6 = threading.Thread(target= (lambda: a.transmit("M_uni 3", 1, 2, 6))) 
thread7 = threading.Thread(target= (lambda: a.transmit("M_uni 4", 2, 3, 8))) 
thread8 = threading.Thread(target= (lambda: a.emit("M3", 3, [1,2,3], [2, 6, 4], [7, 7, 7], [0, 0, 0]))) 
thread9 = threading.Thread(target= (lambda: a.transmit("M_uni 6", 1, 3, 14)))

threads_t = [thread1, thread2, thread3, thread4, thread5, thread6, thread7, thread8, thread9]
while True:
    a.event.wait()
    for thread in threads_t:
        thread.start()
    break

for thread in threads_t:
    thread.join()

clock_thread.join()

print("dv messages 1 = ", a.nodes[1].delivered_messages)
print("dv messages 2 = ", a.nodes[2].delivered_messages)
print("dv messages 3 = ", a.nodes[3].delivered_messages)

