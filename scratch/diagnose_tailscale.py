import sys
import paramiko

host = "192.168.1.200"
username = "jpmorenito"
password = "jpmorenito"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to Raspberry Pi at {host}...")
    ssh.connect(host, username=username, password=password, timeout=5)
    print("Connected successfully!\n")
except Exception as e:
    print(f"Error connecting: {e}")
    sys.exit(1)

commands = [
    ("Tailscale Service Status", f"echo {password} | sudo -S systemctl status tailscaled"),
    ("Tailscale Client Status", f"echo {password} | sudo -S tailscale status"),
    ("Tailscale Network Diagnostic", f"echo {password} | sudo -S tailscale netcheck"),
    ("Tailscale Daemon Logs", f"echo {password} | sudo -S journalctl -u tailscaled -n 30")
]

output_file = "scratch/diagnose_output.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for title, cmd in commands:
        f.write("=" * 60 + "\n")
        f.write(f"RUNNING: {title} ({cmd})\n")
        f.write("=" * 60 + "\n")
        print(f"Executing: {title}...")
        
        try:
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
            
            # Read stdout and stderr
            out_str = stdout.read().decode(errors='ignore')
            err_str = stderr.read().decode(errors='ignore')
            
            f.write("STDOUT:\n")
            f.write(out_str + "\n")
            if err_str:
                f.write("STDERR:\n")
                f.write(err_str + "\n")
        except Exception as e:
            f.write(f"Command execution failed: {e}\n")
        f.write("\n\n")

print(f"Diagnostics completed! Output written to {output_file}")
ssh.close()
