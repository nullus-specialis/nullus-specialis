#!/usr/bin/env python3

import os
import paramiko
from concurrent.futures import ThreadPoolExecutor

def ssh_transfer(hostname):
    # SSH parameters
    ssh_user = 'dshield'
    ssh_port = 12222
    private_key_path = 'dshield-key.pem'

    # Local and remote directory paths
    local_directory = f'packets/{hostname}'
    remote_directory = '/pcap'

    try:
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey(filename=private_key_path)
        ssh.connect(hostname, port=ssh_port, username=ssh_user, pkey=private_key)

        # Change ownership of /pcap and contents to dshield user
        stdin, stdout, stderr = ssh.exec_command(f'sudo chown -R {ssh_user}:{ssh_user} {remote_directory}')

        # Wait for the command to complete
        stdout.channel.recv_exit_status()

        # Create local directory if it doesn't exist
        os.makedirs(local_directory, exist_ok=True)

        # Transfer files from remote to local
        with ssh.open_sftp() as sftp:
            files = sftp.listdir(remote_directory)
            for file in files:
                remote_file_path = f'{remote_directory}/{file}'
                local_file_path = f'{local_directory}/{file}'
                sftp.get(remote_file_path, local_file_path)

        print(f"Transfer completed for {hostname}")

    except Exception as e:
        print(f"Error transferring files for {hostname}: {e}")

    finally:
        ssh.close()

def main():
    # Read hostnames from file
    with open('packetAgents.config', 'r') as file:
        hostnames = [line.strip() for line in file.readlines()]

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=len(hostnames)) as executor:
        executor.map(ssh_transfer, hostnames)

if __name__ == "__main__":
    main()
