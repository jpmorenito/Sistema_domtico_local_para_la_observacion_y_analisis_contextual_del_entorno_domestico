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

# List running docker containers
print("Running 'docker ps':")
stdin, stdout, stderr = ssh.exec_command("docker ps")
print(stdout.read().decode())

# Run docker inspect on esphome to see volume mounts
print("Running 'docker inspect esphome':")
stdin, stdout, stderr = ssh.exec_command("docker inspect esphome")
print(stdout.read().decode())

ssh.close()
