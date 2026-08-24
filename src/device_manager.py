import logging
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeviceManager:
    def __init__(self):
        self.devices = {}
        self.connections = {}

    def add_device(self, name, host, device_type, credentials):
        """Add a new device to the inventory."""
        self.devices[name] = {
            'host': host,
            'device_type': device_type,
            'username': credentials.get('username'),
            'password': credentials.get('password'),
            'secret': credentials.get('secret', '')
        }
        logger.info(f"Added device {name} ({host})")

    def connect(self, device_name):
        """Establish connection to a device."""
        if device_name not in self.devices:
            raise ValueError(f"Device {device_name} not found.")
        
        device = self.devices[device_name]
        try:
            conn = ConnectHandler(**device)
            conn.enable()
            self.connections[device_name] = conn
            logger.info(f"Connected to {device_name}")
            return True
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            logger.error(f"Failed to connect to {device_name}: {str(e)}")
            return False

    def disconnect(self, device_name):
        """Disconnect from a device."""
        if device_name in self.connections:
            self.connections[device_name].disconnect()
            del self.connections[device_name]
            logger.info(f"Disconnected from {device_name}")

    def get_config(self, device_name):
        """Retrieve running configuration."""
        if device_name not in self.connections:
            self.connect(device_name)
        
        conn = self.connections[device_name]
        return conn.send_command("show running-config")

    def get_interfaces(self, device_name):
        """Retrieve interface status."""
        if device_name not in self.connections:
            self.connect(device_name)
            
        conn = self.connections[device_name]
        return conn.send_command("show ip interface brief", use_textfsm=True)

    def get_arp_table(self, device_name):
        """Retrieve ARP table."""
        if device_name not in self.connections:
            self.connect(device_name)
            
        conn = self.connections[device_name]
        return conn.send_command("show arp", use_textfsm=True)

    def get_routing_table(self, device_name):
        """Retrieve routing table."""
        if device_name not in self.connections:
            self.connect(device_name)
            
        conn = self.connections[device_name]
        return conn.send_command("show ip route", use_textfsm=True)

    def backup_config(self, device_name, filepath):
        """Backup configuration to a file."""
        config = self.get_config(device_name)
        with open(filepath, 'w') as f:
            f.write(config)
        logger.info(f"Configuration for {device_name} backed up to {filepath}")
        return True

    def push_config(self, device_name, config_commands):
        """Push configuration commands to a device."""
        if device_name not in self.connections:
            self.connect(device_name)
            
        conn = self.connections[device_name]
        output = conn.send_config_set(config_commands)
        logger.info(f"Pushed config to {device_name}:
{output}")
        return output
