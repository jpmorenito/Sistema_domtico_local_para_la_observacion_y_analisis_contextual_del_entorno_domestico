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

# Read trace.saved_traces
print("Reading trace.saved_traces from the Pi...")
cmd = "echo jpmorenito | sudo -S cat /home/jpmorenito/homeassistant/.storage/trace.saved_traces"
stdin, stdout, stderr = ssh.exec_command(cmd)
# Send password
stdin.write(password + "\n")
stdin.flush()

output = stdout.read().decode()
try:
    data = json.loads(output)
    print(f"Loaded successfully! Keys in trace.saved_traces (count: {len(data)}):")
    # Keys are typically automation_id -> dict of traces
    for k in list(data.keys())[:10]:
        traces = data[k]
        print(f"\nAutomation ID: {k} (number of traces: {len(traces)})")
        if traces:
            first_trace_key = list(traces.keys())[0]
            print(f"  First trace key: {first_trace_key}")
            # print some keys of the trace
            first_trace = traces[first_trace_key]
            print(f"  Trace keys: {list(first_trace.keys())}")
            if 'extended_dict' in first_trace:
                ext = first_trace['extended_dict']
                print(f"    Extended dict keys: {list(ext.keys())}")
                if 'automation_key' in ext:
                    print(f"    Automation key: {ext['automation_key']}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
    # print first 500 chars of output
    print("Raw output (truncated):", output[:500])

ssh.close()
