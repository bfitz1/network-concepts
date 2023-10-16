import socket

def main(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    print(request)
    s.sendall(request.encode("ISO-8859-1"))

    while True:
        response = s.recv(4096)
        if response:
            print(response.decode("ISO-8859-1"), end="")
        else:
            break

    s.close()


if __name__ == '__main__':
    import sys
    
    argcount = len(sys.argv)
    if argcount == 2:
        host, port = sys.argv[1], 80
    elif argcount == 3:
        host, port = sys.argv[1], int(sys.argv[2])
    else:
        print("USAGE: python webclient.py <host> [port]")
        sys.exit(1)

    main(host, port)
    sys.exit(0)
