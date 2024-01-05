#!/usr/bin/env python3

import os
import paramiko
from concurrent.futures import ThreadPoolExecutor

def ssh_transfer_logs(hostname):
    # SSH parameters
    user = 'dshield'
    port = 12222
    private_key_path = '/data/dshieldManager/bin/ssh/dshield-key.pem'

    # Local directory for logs
    local_logs_directory = f'logs/{hostname}'
    os.makedirs(local_logs_directory, exist_ok=True)

    # Connect to the remote host using SSH
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey(filename=private_key_path)
        ssh.connect(hostname, port=port, username=user, pkey=private_key)

        # Transfer log files
        sftp = ssh.open_sftp()
        remote_log_files = sftp.listdir('/logs/')
        for remote_file in remote_log_files:
            if remote_file.startswith('webhoneypot-') and remote_file.endswith('.json'):
                remote_path = f'/logs/{remote_file}'
                local_path = os.path.join(local_logs_directory, remote_file)
                sftp.get(remote_path, local_path)

        sftp.close()
        ssh.close()
        print(f"Logs transferred from {hostname}")
    except Exception as e:
        print(f"Error transferring logs from {hostname}: {e}")

if __name__ == "__main__":
    # Read hostnames from the configuration file
    with open('logAgents.config', 'r') as file:
        hostnames = [line.strip() for line in file.readlines()]

    # Execute SSH transfers in parallel
    with ThreadPoolExecutor(max_workers=len(hostnames)) as executor:
        executor.map(ssh_transfer_logs, hostnames)
