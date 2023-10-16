import socket
import datetime

def main():
    # Step 1: create a socket object.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: connect to the time server on the Time Protocol port.
    sock.connect(('time.nist.gov', 37))

    # Step 3: receive 4 bytes from the server. Sometimes it doesn't work.
    response = sock.recv(1024)
    sock.close()

    # Step 4: decode the bytes into an integer.
    decoded = int.from_bytes(response)

    # Step 5: print the time as reported by the time server and our system.
    print("NIST time: {}".format(decoded))
    print("System time: {}".format(system_seconds_since_1990()))


def system_seconds_since_1990():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(datetime.datetime.now().strftime("%s"))
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

if __name__ == '__main__':
    main()
