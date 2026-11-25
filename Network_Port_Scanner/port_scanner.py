import socket

def scan_port(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        print(f"Port {port} is OPEN on {target_ip}")
    else:
        print(f"Port {port} is CLOSED on {target_ip}")
    sock.close()

if __name__ == "__main__":
    target = "scanme.nmap.org"
    common_ports = [22, 80, 443, 8080]
    print(f"Scanning target: {target}...")
    for p in common_ports:
        scan_port(target, p)
