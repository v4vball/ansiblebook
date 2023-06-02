#!/usr/bin/env python3
""" Vagrant inventory script """
# Adapted from Mark Mandel's implementation
# https://github.com/markmandel/vagrant_ansible_example

import argparse
import io
import json
import subprocess
import sys

import paramiko

# 1. The `parse_args()` function defines the command-line options using `argparse.ArgumentParser`. It sets up two mutually exclusive options: `--list` and `--host`. The `--list` option is used to list all running hosts, while the `--host` option is used to get details for a specific host. The function returns the parsed command-line arguments.
def parse_args():
    """command-line options"""
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()

# 2. The `list_running_hosts()` function is called when the `--list` option is provided. It runs the `vagrant status --machine-readable` command using `subprocess.check_output()` to get the status of all Vagrant machines. It parses the output to extract the running hosts and returns a list of those hosts.

def list_running_hosts():
    """vagrant.py --list function"""
    cmd = ["vagrant", "status", "--machine-readable"]
    status = subprocess.check_output(cmd).rstrip().decode("utf-8")
    hosts = []
    for line in status.splitlines():
        (_, host, key, value) = line.split(',')[:4]
        if key == 'state' and value == 'running':
            hosts.append(host)
    return hosts


# 3. The `get_host_details()` function is called when the `--host` option is provided with a hostname. It runs the `vagrant ssh-config <hostname>` command using `subprocess.check_output()` to get the SSH configuration for the specified host. It uses the `paramiko.SSHConfig` class to parse the SSH configuration and extracts relevant details such as the host, port, username, and private key file. It returns a dictionary containing these details.

def get_host_details(host):
    """vagrant.py --host <hostname> function"""
    cmd = ["vagrant", "ssh-config", host]
    ssh_config = subprocess.check_output(cmd).decode("utf-8")
    config = paramiko.SSHConfig()
    config.parse(io.StringIO(ssh_config))
    host_config = config.lookup(host)
    return {'ansible_host': host_config['hostname'],
            'ansible_port': host_config['port'],
            'ansible_user': host_config['user'],
            'ansible_private_key_file': host_config['identityfile'][0]}


def main():
    """main"""
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({'vagrant': hosts}, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
    main()



# The code you provided is a Python script that serves as a Vagrant inventory script. It uses the `argparse` module to parse command-line arguments and performs different actions based on the specified options. Here's a breakdown of the script:




# 4. The `main()` function is the entry point of the script. It calls `parse_args()` to parse the command-line arguments and performs the corresponding action based on the options. If `--list` is provided, it calls `list_running_hosts()` and outputs the result in JSON format. If `--host` is provided with a hostname, it calls `get_host_details()` and outputs the host details in JSON format.

# 5. Finally, the `if __name__ == '__main__':` block ensures that the `main()` function is only executed if the script is run directly (not imported as a module).

# This script can be used as a custom inventory script for Ansible to dynamically generate an inventory based on the running Vagrant machines. It provides functionality to list running hosts and retrieve their SSH configuration details for Ansible usage.