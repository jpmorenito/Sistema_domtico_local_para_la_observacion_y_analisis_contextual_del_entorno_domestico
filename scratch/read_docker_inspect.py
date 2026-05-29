import sys
import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("100.70.173.44", username="jpmorenito", password="jpmorenito", timeout=5)

stdin, stdout, stderr = ssh.exec_command("docker inspect portainer homeassistant esphome")
data = stdout.read().decode()
try:
    containers = json.loads(data)
    for c in containers:
        name = c["Name"]
        image = c["Config"]["Image"]
        mounts = [m["Source"] + ":" + m["Destination"] for m in c["Mounts"]]
        network = c["HostConfig"]["NetworkMode"]
        ports = c["HostConfig"].get("PortBindings", {})
        print(f"\n--- {name} ---")
        print(f"Image: {image}")
        print(f"Network: {network}")
        print(f"Ports: {ports}")
        print(f"Mounts: {mounts}")
        
except Exception as e:
    print(f"Failed to parse JSON: {e}")
    print(data[:500])

ssh.close()
