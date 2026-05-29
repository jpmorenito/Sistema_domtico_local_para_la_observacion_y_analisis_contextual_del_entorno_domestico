import sys
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host = "100.70.173.44"
username = "jpmorenito"
password = "jpmorenito"

try:
    ssh.connect(host, username=username, password=password, timeout=5)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# List only non-hidden yaml files in /opt/esphome/config (depth 1)
stdin, stdout, stderr = ssh.exec_command("find /opt/esphome/config -maxdepth 1 -name '*.yaml' -o -name '*.yml'")
files = stdout.read().decode().strip().split("\n")

for f in files:
    f = f.strip()
    if f:
        print(f"\nFILE: {f}")
        print("-" * 40)
        stdin, stdout, stderr = ssh.exec_command(f"cat '{f}'")
        print(stdout.read().decode())
        print("-" * 40)

ssh.close()
