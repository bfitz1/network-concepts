import sys
import signal
import socket
import select
import json

def broadcast_message(recipients, packet):
    for r in recipients:
        r.sendall(packet)

def read_and_parse_packet(client):
    length_bytes = bytearray()
    payload_bytes = bytearray()
        
    remaining = 2
    while remaining > 0:
        data = client.recv(remaining)
        length_bytes += data
        remaining -= len(data)

    remaining = int.from_bytes(length_bytes, 'big')
    while remaining > 0:
        data = client.recv(remaining)
        payload_bytes += data
        remaining -= len(data)

    return json.loads(payload_bytes.decode())

def create_response(payload):
    if payload['type'] == 'hello':
        return dict(type='join', nick=payload['nick'])
    elif payload['type'] == 'chat':
        return dict(type='chat', nick=payload['nick'], message=payload['message'])
    else:
        raise ValueError # Not worrying about other cases right now.


def package_response(payload):
    json_str = json.dumps(payload)
    return len(json_str).to_bytes(2, 'big') + json_str.encode()

def run_server(port):
    server = socket.socket()
    server.bind(('', port))
    server.listen()

    read_sockets = set()
    sock_to_nick = dict()
    while True:
        ready_sockets, _, _ = select.select(read_sockets | {server}, {}, {})

        for s in ready_sockets:
            if s is server: # A new connection is ready.
                client, client_info = s.accept()
                read_sockets.add(client)
                print(f"Connection opened by {client_info}.")
                continue
           
            if len(s.recv(2, socket.MSG_PEEK)) == 0: # A connection has closed.
                read_sockets.remove(s)
                nick = sock_to_nick.pop(s)
                packet = package_response(dict(type='leave', nick=nick))
                broadcast_message(read_sockets, packet)
                print(f"Goodbye from '{nick}'.")
                print(f"Connection closed by {s.getpeername()}.")
                continue

            call = read_and_parse_packet(s)
            if call['type'] == 'hello':
                sock_to_nick[s] = call['nick']
                print(f"Hello from '{call['nick']}'.")
                
            response = create_response(call)
            packet = package_response(response)
            broadcast_message(read_sockets, packet)

            print(f"Broadcasting '{response['type']}' message.")

    server.close()

def sigint_handler(sig, frame):
    print("Closing the chat server. Bye!")
    sys.exit(0)

def main(argv):
    signal.signal(signal.SIGINT, sigint_handler)
    
    try:
        port = int(argv[1])
    except:
        print("usage: chatserver.py {host} {port}", file=sys.stderr)
        return 1

    run_server(port)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
