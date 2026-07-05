import paramiko
import sys

def run_ssh_command(host, user, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password, timeout=10)
        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out:
            print("STDOUT:")
            print(out)
        if err:
            print("STDERR:")
            print(err)
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()

def upload_file(host, user, password, local_path, remote_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password, timeout=10)
        sftp = client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        print(f"Successfully uploaded {local_path} to {remote_path}")
    except Exception as e:
        print(f"Upload failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ssh_cmd.py <command> OR python ssh_cmd.py UPLOAD <local> <remote>")
        sys.exit(1)
    
    if sys.argv[1] == "UPLOAD":
        upload_file("100.70.173.44", "jpmorenito", "jpmorenito", sys.argv[2], sys.argv[3])
    else:
        cmd = " ".join(sys.argv[1:])
        run_ssh_command("100.70.173.44", "jpmorenito", "jpmorenito", cmd)
