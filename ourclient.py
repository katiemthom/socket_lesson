import socket
import sys 
import select

def open_connection(host, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((host, port))
    return my_socket

def main():
    my_host = "localhost"
    my_port = 5555
    my_socket = open_connection(my_host, my_port)
    running = True
    while running: 
        inputready, outputready, exceptready = select.select([my_socket, sys.stdin],[],[])

        for s in inputready:
            if s == my_socket:
                msg = s.recv(1024)
                if msg: 
                    if "::" in msg: 
                        print format_message(msg)
                    else: 
                        print msg 
                else: 
                    print "Disconnected from server!"
                    running = False 
            else:
                msg = sys.stdin.readline()
                msg = msg.strip()
                if msg == "/quit":
                    my_socket.close()
                    running = False 
                else:
                    my_socket.sendall(msg)
    my_socket.close()

def format_message(msg):
    tokens = msg.split("::")
    tokens[1] = tokens[1].strip()
    username = tokens[0]
    msg = tokens[1]
    new_msg = "[%s] %s" % (username, msg) 
    return new_msg


main()
