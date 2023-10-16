import socket
import os

def main(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen()

    while True:
        conn, accept = s.accept()
        print("New connection from {addr} on port {port}".format(addr=accept[0], port=accept[1]))

        request = b''

        while True:
            request += conn.recv(4069)
            print(request.decode("ISO-8859-1"))
            if request[-4:] == b"\r\n\r\n":
                break

        if not request.startswith(b"GET"):
            print("I can't tell if this is an HTTP request.")
            continue

        get_line, *rest = request.split(b"\r\n")
        _, path, _ = get_line.split(b" ")
        _, filename = os.path.split(path)

        try:
            with open(filename) as file:
                data = file.read()
        except:
            response = ""
            response += "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type: text/plain\r\n"
            response += "Content-Length: 13\r\n"
            response += "Connection: close\r\n\r\n"
            response += "404 not found"

            conn.sendall(response.encode("ISO-8859-1"))
            conn.close()
            continue

        name, ext = os.path.splitext(filename)
        mime_types = {b".txt": 'text/plain', b".html": 'text/html'}
        content_type = mime_types.get(ext, 'application/octet-stream')

        response = ""
        response += "HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(data)}\r\n"
        response += "Connection: close\r\n\r\n"
        response += data

        print(response)
        conn.sendall(response.encode("ISO-8859-1"))
        conn.close()
        
    s.close()

if __name__ == '__main__':
    import sys

    argcount = len(sys.argv)
    if argcount == 1:
        port = 28333
    elif argcount == 2:
        port = int(sys.argv[1])
    else:
        print("USAGE: python webserver.py [port]")
        sys.exit(1)

    main(port)
    sys.exit(0)
