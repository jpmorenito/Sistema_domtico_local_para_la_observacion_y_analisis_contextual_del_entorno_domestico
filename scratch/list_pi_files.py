import paramiko

host = '100.70.173.44'
user = 'jpmorenito'
password = 'jpmorenito'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(host, username=user, password=password, timeout=10)
    stdin, stdout, stderr = ssh.exec_command('ls -la /home/jpmorenito')
    print("--- ls -la /home/jpmorenito ---")
    print(stdout.read().decode('utf-8'))
    print("--- error ---")
    print(stderr.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
finally:
    ssh.close()
