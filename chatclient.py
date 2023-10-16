import sys
import signal
import socket
import threading
import json

import chatui as ui

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

def parse_message(nick, message):
    if message.startswith('/q'):
        return dict(type='leave', nick=nick)
    elif message.startswith('/message'):
        _, recipient, message = message.split(maxsplit=2)
        return dict(type='direct', nick=nick, recipient=recipient, message=message)
    elif message.startswith("/me"):
        _, message = message.split(maxsplit=1)
        return dict(type='emote', nick=nick, message=message)
    else:
        return dict(type='chat', nick=nick, message=message)

def render_payload(payload):
    if payload['type'] == 'join':
        nick = payload['nick']
        return f"*** {nick} has joined the chat"
    elif payload['type'] == 'chat':
        nick = payload['nick']
        message = payload['message']
        return f"{nick}: {message}"
    elif payload['type'] == 'leave':
        nick = payload['nick']
        return f"*** {nick} has left the chat"
    else:
        raise ValueError # Not worrying about other cases right now.

def handle_incoming(client):
    while True:
        try:
            payload = read_and_parse_packet(client)
        except:
            break
        
        ui.print_message(render_payload(payload))

def run_client(nick, host, port):
    client = socket.socket()
    client.connect((host, port))

    hello = json.dumps(dict(type="hello", nick=nick))
    hello_bytes = len(hello).to_bytes(2, 'big') + hello.encode()
    client.sendall(hello_bytes)

    t1 = threading.Thread(target=handle_incoming, daemon=True, args=(client,))
    t1.start()

    while True:
        message = ui.read_command(f"{nick}> ")
        payload = parse_message(nick, message)

        if payload['type'] == 'leave':
            break
        
        payload_json = json.dumps(payload)
        packet = len(payload_json).to_bytes(2, 'big') + payload_json.encode()
        client.sendall(packet)

    client.close()

def sigint_handler(sig, frame):
    ui.end_windows()
    sys.exit(0)

def main(argv):
    signal.signal(signal.SIGINT, sigint_handler)

    try:
        nick = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        print("usage: chatclient.py {nick} {host} {port}", file=sys.stderr)
        return 1

    ui.init_windows()
    run_client(nick, host, port)
    ui.end_windows()
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
