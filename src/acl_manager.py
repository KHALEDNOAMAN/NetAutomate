import logging
from .device_manager import DeviceManager

logger = logging.getLogger(__name__)

class ACLManager:
    def __init__(self, device_manager: DeviceManager):
        self.dm = device_manager

    def validate_rules(self, rules):
        """Validate syntax of ACL rules (basic implementation)."""
        valid_actions = ['permit', 'deny']
        valid_protocols = ['ip', 'tcp', 'udp', 'icmp']
        
        for rule in rules:
            parts = rule.split()
            if len(parts) < 4:
                return False
            action, protocol, src, dst = parts[0], parts[1], parts[2], parts[3]
            if action not in valid_actions or protocol not in valid_protocols:
                return False
        return True

    def create_acl(self, device_name, name, rules):
        """Create an ACL on a device."""
        if not self.validate_rules(rules):
            raise ValueError("Invalid ACL rules provided.")
            
        commands = [f"ip access-list extended {name}"]
        commands.extend(rules)
        
        logger.info(f"Creating ACL {name} on {device_name}")
        return self.dm.push_config(device_name, commands)

    def apply_acl(self, device_name, interface, direction, acl_name):
        """Apply an ACL to an interface."""
        if direction not in ['in', 'out']:
            raise ValueError("Direction must be 'in' or 'out'")
            
        commands = [
            f"interface {interface}",
            f"ip access-group {acl_name} {direction}"
        ]
        logger.info(f"Applying ACL {acl_name} ({direction}) to {interface} on {device_name}")
        return self.dm.push_config(device_name, commands)

    def remove_acl(self, device_name, acl_name):
        """Remove an ACL from a device."""
        commands = [f"no ip access-list extended {acl_name}"]
        logger.info(f"Removing ACL {acl_name} from {device_name}")
        return self.dm.push_config(device_name, commands)

    def show_acl(self, device_name):
        """Retrieve ACL information from a device."""
        if device_name not in self.dm.connections:
            self.dm.connect(device_name)
            
        conn = self.dm.connections[device_name]
        return conn.send_command("show access-lists")

    def generate_acl_from_policy(self, policy_file):
        """Generate ACL commands from a YAML policy file."""
        import yaml
        with open(policy_file, 'r') as f:
            policy = yaml.safe_load(f)
            
        rules = []
        for rule in policy.get('rules', []):
            action = rule.get('action')
            protocol = rule.get('protocol')
            src = rule.get('src')
            dst = rule.get('dst')
            port = rule.get('port', '')
            
            rule_str = f"{action} {protocol} {src} {dst}"
            if port:
                rule_str += f" eq {port}"
            rules.append(rule_str)
            
        return policy.get('name'), rules
