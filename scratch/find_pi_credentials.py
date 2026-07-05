import sys
import paramiko

ips = ['192.168.1.12', '192.168.1.75', '192.168.1.77']
username = "jpmorenito"
password = "jpmorenito"

for ip in ips:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Trying to connect to {ip}...")
        ssh.connect(ip, username=username, password=password, timeout=2)
        print(f"SUCCESS! The Raspberry Pi is at: {ip}")
        # Run hostname to verify
        stdin, stdout, stderr = ssh.exec_command("hostname")
        print(f"Hostname: {stdout.read().decode().strip()}")
        ssh.close()
        break
    except Exception as e:
        print(f"Failed for {ip}: {e}")
