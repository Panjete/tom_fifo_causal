from abcast import abcast_node, abcast_system

a = abcast_system(3)
a.nodes[1].local_timestamp = 0
a.nodes[2].local_timestamp = 1
a.nodes[3].local_timestamp = 3

a.emit("first node sends", 0, [1,2,3])
a.emit("second node sends", 0, [1,2,3])
a.emit("third node sends", 0, [1,2,3])

print("dv messages 1 = ", a.nodes[1].delivered_messages)
print("dv messages 2 = ", a.nodes[2].delivered_messages)
print("dv messages 3 = ", a.nodes[3].delivered_messages)

