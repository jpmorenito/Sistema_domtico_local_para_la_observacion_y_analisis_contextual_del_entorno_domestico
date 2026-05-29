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

print("Searching for files containing 'escritorio' on the Pi:")
stdin, stdout, stderr = ssh.exec_command("find /opt/esphome -name '*escritorio*'")
print(stdout.read().decode())

ssh.close()
