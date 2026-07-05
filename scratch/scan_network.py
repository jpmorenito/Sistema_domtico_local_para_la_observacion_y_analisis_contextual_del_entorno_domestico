import socket
from concurrent.futures import ThreadPoolExecutor

subnet = "192.168.1."
port = 22

def check_ip(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    try:
        s.connect((ip, port))
        print(f"FOUND SSH ON: {ip}")
        return ip
    except Exception:
        return None
    finally:
        s.close()

ips_to_check = [f"{subnet}{i}" for i in range(2, 255)]

print(f"Scanning subnet {subnet}0/24 for open SSH port 22...")
with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(check_ip, ips_to_check)

found_ips = [r for r in results if r is not None]
print(f"Scan complete. Active SSH IPs found: {found_ips}")
