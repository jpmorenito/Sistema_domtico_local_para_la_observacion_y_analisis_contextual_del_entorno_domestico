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

# Check docker compose files or docker run commands
commands = [
    "docker ps",
    "sudo find /opt -name 'docker-compose.yml' -o -name 'compose.yml'",
    "sudo find /home -name 'docker-compose.yml' -o -name 'compose.yml'",
    "cat /opt/docker-compose.yml",
    "cat /home/jpmorenito/docker-compose.yml"
]

for cmd in commands:
    print(f"\n==================================================")
    print(f"Running: {cmd}")
    print(f"==================================================")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(f"Error: {err}")

ssh.close()
