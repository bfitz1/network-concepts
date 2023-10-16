import sys
import json

def ipv4_to_value(ipv4_addr):
    """
    Convert a dots-and-numbers IP address to a single 32-bit numeric
    value of integer type. Returns an integer type.

    Example:

    ipv4_addr: "255.255.0.0"
    return:    4294901760  (Which is 0xffff0000 hex)

    ipv4_addr: "1.2.3.4"
    return:    16909060  (Which is 0x01020304 hex)
    """

    value = 0
    for i, x in enumerate(reversed(ipv4_addr.split('.')), ):
        value += int(x) << (8*i)

    return value

def value_to_ipv4(addr):
    """
    Convert a single 32-bit numeric value of integer type to a
    dots-and-numbers IP address. Returns a string type.

    Example:

    There is only one input value, but it is shown here in 3 bases.

    addr:   0xffff0000 0b11111111111111110000000000000000 4294901760
    return: "255.255.0.0"

    addr:   0x01020304 0b00000001000000100000001100000100 16909060
    return: "1.2.3.4"
    """

    value = []
    for _ in range(4):
        value.append(str(addr & 0xff))
        addr = addr >> 8

    return '.'.join(reversed(value))

def get_subnet_mask_value(slash):
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number of integer type. The input can contain an IP
    address optionally, but that part should be discarded.

    Returns an integer type.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111111111110000000000000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """

    _, _, bitstr = slash.partition('/')
    bits = int(bitstr)
    return (((1 << bits) - 1) << (32 - bits)) & 0xffffffff

def ips_same_subnet(ip1, ip2, slash):
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notataion, return true if the two IP addresses are on the same
    subnet.

    Returns a boolean.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """

    value1 = ipv4_to_value(ip1)
    value2 = ipv4_to_value(ip2)
    mask = get_subnet_mask_value(slash)

    return (value1 & mask) == (value2 & mask)

def get_network(ip_value, netmask):
    """
    Return the network portion of an address value as integer type.

    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300
    """

    return ip_value & netmask

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """

    for router_ip, data in routers.items():
        if ips_same_subnet(ip, router_ip, data['netmask']):
            return router_ip

    return None

# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!
"""
def my_tests():
    print("-------------------------------------")
    print("This is the result of my custom tests")
    print("-------------------------------------")

    # print(x)

    # Add custom test code here
    print("Testing ipv4_to_value:")
    for addr in ['255.255.0.0', '1.2.3.4']:
        value = ipv4_to_value(addr)
        print(f"\t{addr} => {value} 0x{value:x}")

    print("Testing value_to_ipv4:")
    for value in [4294901760, 16909060]:
        addr = value_to_ipv4(value)
        print(f"\t{value} => {addr}")

    print("Testing get_subnet_mask_value:")
    for slash in ['/16', '10.20.30.40/23']:
        mask = get_subnet_mask_value(slash)
        print(f"\t{slash} => 0x{mask:08x} 0b{mask:032b} {mask}")

    print("Testing ips_same_subnet:")
    test_values = [
        ('10.23.121.17', '10.23.121.225', '/23'),
        ('10.23.230.22', '10.24.121.225', '/16'),
    ]
    for ip1, ip2, slash in test_values:
        result = ips_same_subnet(ip1, ip2, slash)
        print(f"\t({ip1}, {ip2}, {slash}) => {result}")

    print("Testing get_network:")
    for ip_value, netmask in [(0x01020304, 0xffffff00)]:
        result = get_network(ip_value, netmask)
        print(f"\t(0x{ip_value:08x}, 0x{netmask:08x}) => 0x{result:08x}")

    print("Testing find_router_for_ip:")
    test_values = [
        ({ '1.2.3.1': { 'netmask': '/24' },
           '1.2.4.1': { 'netmask': '/24' }, }, '1.2.3.5'),
        ({ '1.2.3.1': { 'netmask': '/24' },
           '1.2.4.1': { 'netmask': '/24' }, }, '1.2.5.6'),
    ]
    for routers, ip in test_values:
        result = find_router_for_ip(routers, ip)
        print(f"\t({routers}, {ip}) => {result}")
"""

## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = str(find_router_for_ip(routers, ip))
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
