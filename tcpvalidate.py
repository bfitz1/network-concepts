def ipaddr_to_bytes(addr):
    return b''.join(int(x).to_bytes(1, 'big') for x in addr.split('.'))

def pseudoheader_bytes(source, destination, length):
    return b''.join([
        ipaddr_to_bytes(source),
        ipaddr_to_bytes(destination),
        b'\x00',
        b'\x06',
        length.to_bytes(2, 'big')
    ])

def chunks(data):
    if len(data) % 2 == 1:
        data += b'\x00'

    offset = 0
    while offset < len(data):
        yield int.from_bytes(data[offset:offset + 2], 'big')
        offset += 2

def checksum(header, tcp_data):
    data = header + tcp_data

    total = 0
    for word in chunks(data):
        total += word
        total = (total & 0xffff) + (total >> 16)

    return (~total) & 0xffff

for i in range(10):
    with open(f'tcp_data/tcp_addrs_{i}.txt', 'r') as file:
        line = file.readline().strip()
        source, destination = line.split(' ')

    with open(f'tcp_data/tcp_data_{i}.dat', 'rb') as file:
        tcp_data = file.read()
        tcp_length = len(tcp_data)

    tcp_zero_chksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]

    header = pseudoheader_bytes(source, destination, tcp_length)
    old_chk = int.from_bytes(tcp_data[16:18], 'big')
    new_chk = checksum(header, tcp_zero_chksum)

    if old_chk == new_chk:
        print("PASS")
    else:
        print("FAIL")
