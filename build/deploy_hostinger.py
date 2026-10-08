import os
import paramiko
import time

HOST = "147.93.42.26"
PORT = 65002
USER = "u725432670"
PASS = "asdfafssa@#@!12F"

LOCAL_SITE_DIR = r"c:\Users\moham\OneDrive\Desktop\Websites\elite-arch\site"
TARGET_DIRS = [
    "domains/blueviolet-caterpillar-877701.hostingersite.com/public_html",
    "domains/elitearchitecturegy.com/public_html"
]

import sys
import io
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def log(msg):
    print(msg, flush=True)

class HostingerSession:
    def __init__(self):
        self.client = None
        self.sftp = None

    def connect(self):
        try:
            if self.sftp: self.sftp.close()
            if self.client: self.client.close()
        except Exception:
            pass
        log(f"Connecting to Hostinger SSH {USER}@{HOST}:{PORT}...")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(HOST, port=PORT, username=USER, password=PASS, timeout=25)
        self.sftp = self.client.open_sftp()
        log("SSH & SFTP connection established.")

    def ensure_remote_dir(self, remote_dir):
        dirs_to_create = []
        current = remote_dir
        while current and current != "/":
            try:
                self.sftp.stat(current)
                break
            except Exception:
                dirs_to_create.append(current)
                current = os.path.dirname(current)
        for d in reversed(dirs_to_create):
            try:
                self.sftp.mkdir(d)
            except Exception:
                pass

    def upload_file_with_retry(self, local_file, remote_file):
        for attempt in range(5):
            try:
                self.ensure_remote_dir(os.path.dirname(remote_file))
                self.sftp.put(local_file, remote_file, confirm=False)
                return True
            except Exception as e:
                log(f"  Connection issue during upload ({e}). Reconnecting (attempt {attempt+1}/5)...")
                time.sleep(1)
                try:
                    self.connect()
                except Exception:
                    pass
        return False

    def upload_folder(self, local_dir, remote_dir):
        log(f"Deploying {local_dir} -> {remote_dir}...")
        uploaded_count = 0
        skipped_count = 0
        start_time = time.time()

        for root, dirs, files in os.walk(local_dir):
            rel_path = os.path.relpath(root, local_dir)
            target_remote = remote_dir if rel_path == "." else os.path.join(remote_dir, rel_path).replace("\\", "/")
            self.ensure_remote_dir(target_remote)

            for f in files:
                local_file = os.path.join(root, f)
                remote_file = os.path.join(target_remote, f).replace("\\", "/")

                should_upload = True
                try:
                    local_size = os.path.getsize(local_file)
                    remote_stat = self.sftp.stat(remote_file)
                    if remote_stat.st_size == local_size:
                        should_upload = False
                except Exception:
                    should_upload = True

                if should_upload:
                    success = self.upload_file_with_retry(local_file, remote_file)
                    if success:
                        uploaded_count += 1
                        if uploaded_count % 25 == 0:
                            log(f"  [{os.path.basename(remote_dir)}] Uploaded {uploaded_count} files...")
                    else:
                        log(f"  ERROR: Failed to upload {remote_file}")
                else:
                    skipped_count += 1

        duration = time.time() - start_time
        log(f"Finished {remote_dir}: {uploaded_count} uploaded, {skipped_count} already up-to-date ({duration:.1f}s)")

    def close(self):
        try:
            if self.sftp: self.sftp.close()
            if self.client: self.client.close()
        except Exception:
            pass

session = HostingerSession()
try:
    session.connect()
    
    for target in TARGET_DIRS:
        log(f"\n==========================================")
        log(f"Target: {target}")
        log(f"==========================================")
        
        default_php = f"{target}/default.php"
        try:
            session.sftp.remove(default_php)
            log(f"Removed Hostinger default.php from {target}")
        except Exception:
            pass

        session.upload_folder(LOCAL_SITE_DIR, target)

    htaccess_content = """# Hostinger Static Site Config
Options -Indexes
DirectoryIndex index.html

<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule ^404$ /404.html [L]
</IfModule>

# Caching & Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json image/svg+xml
</IfModule>
"""
    for target in TARGET_DIRS:
        try:
            stdin, stdout, stderr = session.client.exec_command(f'cat << "EOF" > {target}/.htaccess\n{htaccess_content}\nEOF\n')
            stdout.read()
        except Exception:
            pass

    log("\n🎉 Deployment to all Hostinger domains completed successfully!")

finally:
    session.close()
