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

# List files in Home Assistant's .storage directory
print("Listing .storage files on the Raspberry Pi...")
cmd = "echo jpmorenito | sudo -S ls -la /home/jpmorenito/homeassistant/.storage/"
stdin, stdout, stderr = ssh.exec_command(cmd)
# Send password
stdin.write(password + "\n")
stdin.flush()
print(stdout.read().decode())

# Check specifically for trace.saved_traces
print("\nChecking for trace.saved_traces...")
cmd = "echo jpmorenito | sudo -S ls -la /home/jpmorenito/homeassistant/.storage/trace.saved_traces"
stdin, stdout, stderr = ssh.exec_command(cmd)
# Send password
stdin.write(password + "\n")
stdin.flush()
print(stdout.read().decode())

ssh.close()
