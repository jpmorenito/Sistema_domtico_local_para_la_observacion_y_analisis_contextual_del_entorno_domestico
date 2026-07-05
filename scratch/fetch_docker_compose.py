import paramiko

host = '100.70.173.44'
user = 'jpmorenito'
password = 'jpmorenito'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(host, username=user, password=password, timeout=10)
    stdin, stdout, stderr = ssh.exec_command('cat /home/jpmorenito/docker-compose.yml')
    out = stdout.read()
    if out:
        with open('pi_docker_compose.yml', 'wb') as f:
            f.write(out)
        print("Downloaded /home/jpmorenito/docker-compose.yml to pi_docker_compose.yml")
    else:
        print("docker-compose.yml empty or not found on remote")
except Exception as e:
    print("Error:", str(e))
finally:
    ssh.close()
