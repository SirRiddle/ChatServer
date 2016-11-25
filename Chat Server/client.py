# client coded by SirRiddle
import socket
import select
import sys
import getpass

HOST = '0.0.0.0'
PORT = 65420


def Main():
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.settimeout(1)

    try:
        main_socket.connect((HOST, PORT))
    except:
        print('Looks like server is offline')
        sys.exit()
    print('Connected successfully *Now you can start chatting*')
    sys.stdout.write('->');
    sys.stdout.flush()
    while True:
        sock_list = [sys.stdin, main_socket]
        try:
            read, write, error = select.select(sock_list, [], [])
        except:
            print('Client Disconnected')
            sys.exit()

        for sock in read:
            if sock == main_socket:
                data = sock.recv(4096)
                if not data:
                    print('Disconnected from chat server')
                    sys.exit()
                else:
                    message = data.decode('utf-8')
                    print(message, end='')
                    sys.stdout.write('->');
                    sys.stdout.flush()
            else:
                message = sys.stdin.readline()
                message = str(getpass.getuser()).capitalize() + '-> ' + message
                main_socket.send(message.encode('utf-8'))
                sys.stdout.write('->');
                sys.stdout.flush()

    main_socket.close()

if __name__ == '__main__':
    Main()
