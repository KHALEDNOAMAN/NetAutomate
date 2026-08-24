# NetAutomate - Network Automation Toolkit

A comprehensive toolkit for network device management, VLAN provisioning, ACL management, and configuration backup.

## Overview
NetAutomate is a Python-based automation toolkit designed to simplify network operations. It provides a modular approach to managing network infrastructure, supporting multiple vendors through standard protocols.

## Features
- **Device Management**: Connect, retrieve configurations, and gather operational data (interfaces, ARP, routing).
- **VLAN Provisioning**: Automate VLAN creation, deletion, and port assignments.
- **ACL Management**: Define, apply, and validate Access Control Lists.
- **Configuration Backup & Diff**: Schedule backups, compare configurations, and check compliance.
- **CLI Interface**: Easy-to-use command-line interface for all operations.

## Architecture
NetAutomate uses `netmiko` and `napalm` for device connectivity. Jinja2 templates define standard configurations, which are pushed to devices.

## Tech Stack
- Python 3.8+
- Netmiko, NAPALM, Paramiko
- Jinja2, PyYAML, TextFSM
- Rich, Click (for CLI)

## Installation
```bash
git clone https://github.com/KHALEDNOAMAN/NetAutomate.git
cd NetAutomate
pip install -r requirements.txt
python setup.py install
```

## Usage
```bash
netautomate devices list
netautomate vlans create --vlan 10 --name "Users" --device "switch-01"
netautomate backup run --all
```

## Screenshots
```text
+---------------------------------------------------+
| NetAutomate CLI - Device Status                   |
+---------------------------------------------------+
| Device      | IP Address   | Status | Last Backup |
| switch-01   | 10.0.1.1     | ONLINE | 2 hrs ago   |
| router-01   | 10.0.0.1     | ONLINE | 1 hr ago    |
+---------------------------------------------------+
```

## Roadmap
- REST API support
- Ansible integration
- Web Dashboard

## License
MIT License
