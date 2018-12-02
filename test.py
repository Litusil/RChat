import socket, pickle
import struct

class message:
    msg = ""
    def __init__(self, msg):
        self.msg = msg

class join:
    name = ""
    def __init__(self, name):
        self.name = name

class exit:
    exit = "ByeBye"

msg = input("What is your name ?")

HOST = 'localhost'
PORT = 50000
# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

variable1 = join('geiler typ')
packet1 = pickle.dumps(variable1)
length1 = struct.pack('!I', len(packet1))
packet1 = length1 + packet1

variable2 = message('1 nicer message von messagzität her')
packet2 = pickle.dumps(variable2)
length2 = struct.pack('!I', len(packet2))
packet2 = length2 + packet2

s.send(packet1)

for x in range(1,10):
    s.send(packet2)

print ('Data Sent to Server')