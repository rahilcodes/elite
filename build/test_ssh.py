import paramiko

host = "147.93.42.26"
port = 65002
username = "u725432670"
password = "asdfafssa@#@!12F"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to SSH {username}@{host}:{port}...")
    client.connect(host, port=port, username=username, password=password, timeout=15)
    print("SSH Connection successful!")

    stdin, stdout, stderr = client.exec_command("pwd; ls -la; find . -maxdepth 3 -name public_html")
    print("Remote Output:")
    print(stdout.read().decode())
    print("Remote Errors:")
    print(stderr.read().decode())

finally:
    client.close()
