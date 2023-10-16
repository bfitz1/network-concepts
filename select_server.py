# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    s = socket.socket()
    s.bind(('', port))
    s.listen()

    read_sockets = {s}
    while True:
        ready_read, _, _ = select.select(read_sockets, {}, {})

        for sock in ready_read:
            if sock is s: 
                client, clientinfo = sock.accept()
                read_sockets.add(client)

                print(f"{clientinfo}: connected")
            else:
                data = sock.recv(4096)
                if len(data) == 0:
                    read_sockets.remove(sock)
                    print(f"{sock.getpeername()}: disconnected")
                else:
                    print(f"{sock.getpeername()} {len(data)} bytes: {data}")

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
