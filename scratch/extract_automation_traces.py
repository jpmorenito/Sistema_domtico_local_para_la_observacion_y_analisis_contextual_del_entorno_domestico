import sys
import paramiko
import json

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

cmd = "echo jpmorenito | sudo -S cat /home/jpmorenito/homeassistant/.storage/trace.saved_traces"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdin.write(password + "\n")
stdin.flush()

output = stdout.read().decode()
try:
    full_data = json.loads(output)
    ha_data = full_data.get("data", {})
    print(f"Total automations with traces: {len(ha_data)}")
    for auto_id, traces in ha_data.items():
        print(f"\nAutomation: {auto_id} ({len(traces)} traces)")
        for idx, t in enumerate(traces[:3]): # Show up to 3 traces
            ext = t.get("extended_dict", {})
            timestamp = ext.get("timestamp", {})
            start_time = timestamp.get("start", "Unknown")
            run_id = ext.get("run_id", "Unknown")
            state = ext.get("state", "Unknown")
            print(f"  Trace #{idx+1}: start={start_time}, state={state}, run_id={run_id}")
except Exception as e:
    print(f"Error: {e}")

ssh.close()
