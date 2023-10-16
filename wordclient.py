import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2
MAX_BYTES = 1024

packet_buffer = b''

def is_complete_packet():
    global packet_buffer

    if len(packet_buffer) < 2:
        return False

    word_len = int.from_bytes(packet_buffer[:2], 'big')
    return len(packet_buffer) >= 2 + word_len

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung up.
    """

    global packet_buffer

    while not is_complete_packet():
        data = s.recv(MAX_BYTES)
        if len(data) == 0:
            return None

        packet_buffer += data

    word_len = int.from_bytes(packet_buffer[:2], 'big')
    end = 2 + word_len
    word_packet = packet_buffer[:end]
    packet_buffer = packet_buffer[end:]

    return word_packet

def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    word = word_packet[2:]
    return word.decode()

def main(host, port):
    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)
        if word_packet is None:
            break

        word = extract_word(word_packet)
        print(f"\t{word}")

    s.close()

if __name__ == '__main__':
    import sys

    args = sys.argv[1:]
    try:
        host, port = args[0], int(args[1])
    except:
        print("usage: wordclient.py <server> <port>", file=sys.stderr)
        sys.exit(1)

    main(host, port)
    sys.exit(0)
