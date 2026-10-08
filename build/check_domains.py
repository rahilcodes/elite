import paramiko

host = "147.93.42.26"
port = 65002
username = "u725432670"
password = "asdfafssa@#@!12F"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port=port, username=username, password=password, timeout=15)
    
    cmd = """
    echo "=== blueviolet ==="
    ls -la domains/blueviolet-caterpillar-877701.hostingersite.com/public_html
    echo "=== elitearchitecturegy ==="
    ls -la domains/elitearchitecturegy.com/public_html
    """
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
finally:
    client.close()
