# this is a TCP server made by SirRiddle
import socket
import select
import sys

HOST = '0.0.0.0'
PORT = 65420
SOCK_LIST = []


def bc_message(client, server_socket, message):
    for sock in SOCK_LIST:
        if sock != server_socket and sock != client:
            try:
                sock.send(message.encode('utf-8'))
            except:
                sock.close()
                if sock in SOCK_LIST:
                    SOCK_LIST.remove(sock)


def Main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(6)
    SOCK_LIST.append(server_socket)
    print('Server started :)')
    while True:
        try:
            read, write, error = select.select(SOCK_LIST, [], [], 0)
        except:
            print('Server Disconnected')
            sys.exit()
        for sock in read:
            if sock == server_socket:
                client, address = server_socket.accept()
                SOCK_LIST.append(client)
                print('Client ({0},{1}) connected'.format(address[0], address[1]))
                bc_message(client, server_socket, '({0},{1}) has entered chat\n'.format(address[0], address[1]))
            else:
                try:
                    data = sock.recv(4096).decode('utf-8')
                    if data:
                        message = '[{}:{}]:{}'.format(address[0], address[1], data)
                        print(message, end='')
                        bc_message(sock, server_socket, message)
                    else:
                        if sock in SOCK_LIST:
                            sock.close()
                            SOCK_LIST.remove(sock)

                        print('Client ({0}, {1}) disconnected.'.format(address[0], address[1]))
                        bc_message(sock, server_socket, 'User ({0},{1}) has gone offline\n'.format(address[0],address[1]))
                except:
                    print('Client ({0}, {1}) disconnected.'.format(address[0], address[1]))
                    bc_message(sock, server_socket, 'User ({0},{1}) has gone offline\n'.format(address[0], address[1]))
                    continue
    server_socket.close()

if __name__ == '__main__':
    Main()
