import socket, pickle
import struct
import threading

HOST = 'localhost'
PORT = 50000
NAME = ""
DICT = dict()

class message:
    msg = ""
    def __init__(self, msg):
        self.msg = msg

class join:
    name = ""
    def __init__(self, name):
        self.name = name

def listPartner():
    print('test')


def scan():
    scanThreads = []
    for x in range(1, 60):
        t = threading.Thread(target=scanConnection, args=(x,))
        scanThreads.append(t)
    for x in scanThreads:
        x.start()
    for x in scanThreads:
        x.join()
    print("scan completed")


def scanConnection(ip_endung):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        ip = '141.37.168.' + str(ip_endung)
        sock.connect((ip, PORT))
        sock.close()
    except socket.error:
        pass


def createJoin():
    joinMsg = join(NAME)
    joinPacket = pickle.dumps(joinMsg)
    lengthJoinPacket = struct.pack('!I', len(joinPacket))
    return lengthJoinPacket + joinPacket


def createMessage(messageString):
    msg = message(messageString)
    messagePacket = pickle.dumps(msg)
    lengthMessagePacket = struct.pack('!I', len(messagePacket))
    return lengthMessagePacket + messagePacket


def parser():
    while True:
        msg = input(":")
        if msg[0] == 's':
            scan()
        elif msg[0] == 'l':
            listPartner()
        elif msg[0] == 'c':
            msgArr= msg.split(' ',3)
            conn = DICT.get(msgArr[1])
            conn.send(createMessage(msgArr[2]))
        elif msg[0] == 'g':
            msgArr = (msg.split(' ',2))
            msg = createMessage(msgArr[1])
            for x in DICT.values():
                x.send(msg)
        elif msg[0] == 'q':
            print('I QUIT')
            exit


def new_client_connection(conn,addr):
    connected = True
    namePartner = ""
    while connected:
        try:
            buf = b''
            while len(buf) < 4:
                buf += conn.recv(4 - len(buf))
            length = struct.unpack('!I', buf)[0]

            packet = conn.recv(length)

            data_variable = pickle.loads(packet)

            if type(data_variable) is message:
                print('{}: {}'.format(namePartner,data_variable.msg))

            if type(data_variable) is join:
                namePartner = data_variable.name
                DICT[data_variable.name] = conn
                conn.send(createJoin());
        except (ConnectionAbortedError,ConnectionResetError) :
            print("Verbindung von {} getrennt".format(addr))
            connected = False

name = input("Bitte Name angeben:")
NAME = name

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

komm = threading.Thread(target=parser)
komm.start()

while True:
    conn, addr = s.accept()
    print('Connected by', addr)

    test = threading.Thread(target=new_client_connection,args=(conn, addr))
    test.start()

s.close()






