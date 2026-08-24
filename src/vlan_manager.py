import logging
from .device_manager import DeviceManager

logger = logging.getLogger(__name__)

class VLANManager:
    def __init__(self, device_manager: DeviceManager):
        self.dm = device_manager

    def create_vlan(self, device_name, vlan_id, name):
        """Create a VLAN on a device."""
        commands = [
            f"vlan {vlan_id}",
            f"name {name}"
        ]
        logger.info(f"Creating VLAN {vlan_id} ({name}) on {device_name}")
        return self.dm.push_config(device_name, commands)

    def delete_vlan(self, device_name, vlan_id):
        """Delete a VLAN from a device."""
        commands = [f"no vlan {vlan_id}"]
        logger.info(f"Deleting VLAN {vlan_id} on {device_name}")
        return self.dm.push_config(device_name, commands)

    def assign_port_to_vlan(self, device_name, interface, vlan_id):
        """Assign an access port to a VLAN."""
        commands = [
            f"interface {interface}",
            "switchport mode access",
            f"switchport access vlan {vlan_id}"
        ]
        logger.info(f"Assigning {interface} to VLAN {vlan_id} on {device_name}")
        return self.dm.push_config(device_name, commands)

    def trunk_port(self, device_name, interface, allowed_vlans):
        """Configure a port as a trunk and set allowed VLANs."""
        commands = [
            f"interface {interface}",
            "switchport trunk encapsulation dot1q",
            "switchport mode trunk",
            f"switchport trunk allowed vlan {allowed_vlans}"
        ]
        logger.info(f"Configuring trunk on {interface} with VLANs {allowed_vlans} on {device_name}")
        return self.dm.push_config(device_name, commands)

    def show_vlans(self, device_name):
        """Retrieve VLAN information from a device."""
        if device_name not in self.dm.connections:
            self.dm.connect(device_name)
        
        conn = self.dm.connections[device_name]
        return conn.send_command("show vlan brief", use_textfsm=True)

    def generate_vlan_report(self):
        """Generate a report of VLANs across all devices."""
        report = {}
        for device_name in self.dm.devices:
            try:
                vlans = self.show_vlans(device_name)
                report[device_name] = vlans
            except Exception as e:
                logger.error(f"Failed to get VLANs for {device_name}: {str(e)}")
                report[device_name] = []
        return report
