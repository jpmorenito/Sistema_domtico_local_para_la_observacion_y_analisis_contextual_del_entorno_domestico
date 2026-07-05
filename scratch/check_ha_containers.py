import sys
import paramiko

host = "192.168.1.77"
username = "jpmorenito"
password = "jpmorenito"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=username, password=password, timeout=5)
except Exception as e:
    print(f"Error connecting: {e}")
    sys.exit(1)

commands = [
    ("List Docker Containers", "docker ps"),
    ("Inspect Home Assistant Volumes", "docker inspect homeassistant --format='{{json .Mounts}}'")
]

for title, cmd in commands:
    print("=" * 60)
    print(title)
    print("=" * 60)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
         print("STDERR:", err)

ssh.close()
