from abcast import abcast_node, abcast_system
import threading

a = abcast_system(2)

clock_thread = threading.Thread(target=a.start_global_clock) ## global clock
clock_thread.daemon = True  # Making it a daemon thread so that it doesn't block the main program
clock_thread.start()

## Co-ordinating time-delays so that  so that 
thread1 = threading.Thread(target= (lambda: a.emit("M1", 1, [1,2], [0, 1], [0, 1], [0, 1]))) 
thread2 = threading.Thread(target= (lambda: a.emit("M2", 2, [1,2], [2, 2], [2, 2], [2, 2]))) 
thread3 = threading.Thread(target= (lambda: a.emit("M3", 1, [1,2], [0, 1], [0, 1], [0, 1]))) 

while True:
    a.event.wait()
    threads_t = [thread1, thread2, thread3]
    for thread in threads_t:
        thread.start()
    break

for thread in threads_t:
    thread.join()

clock_thread.join()

print("dv messages 1 = ", a.nodes[1].delivered_messages)
print("dv messages 2 = ", a.nodes[2].delivered_messages)


