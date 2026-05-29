import sys
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host = "100.70.173.44"
username = "jpmorenito"
password = "jpmorenito"

try:
    print(f"Connecting to {host}...")
    ssh.connect(host, username=username, password=password, timeout=5)
    print("Connected successfully!")
except Exception as e:
    print(f"Error connecting: {e}")
    sys.exit(1)

# Find all yaml files in the home directory
print("Running find for yaml files in /home/jpmorenito:")
stdin, stdout, stderr = ssh.exec_command("find /home/jpmorenito -name '*.yaml' -o -name '*.yml'")
print(stdout.read().decode())

ssh.close()
