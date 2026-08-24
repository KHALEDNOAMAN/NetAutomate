import logging
import os
import time
import difflib
from datetime import datetime
from .device_manager import DeviceManager

logger = logging.getLogger(__name__)

class ConfigBackup:
    def __init__(self, device_manager: DeviceManager, backup_dir="backups"):
        self.dm = device_manager
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup_all(self, devices):
        """Backup configuration for all specified devices."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {}
        
        for device in devices:
            filepath = os.path.join(self.backup_dir, f"{device}_{timestamp}.cfg")
            try:
                self.dm.backup_config(device, filepath)
                results[device] = filepath
            except Exception as e:
                logger.error(f"Backup failed for {device}: {str(e)}")
                results[device] = None
        return results

    def schedule_backup(self, interval_hours):
        """Schedule periodic backups (simplified loop)."""
        logger.info(f"Starting scheduled backups every {interval_hours} hours")
        devices = list(self.dm.devices.keys())
        while True:
            self.backup_all(devices)
            time.sleep(interval_hours * 3600)

    def compare_configs(self, config1_path, config2_path):
        """Compare two configuration files and return diff."""
        with open(config1_path, 'r') as f1, open(config2_path, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            
        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile=os.path.basename(config1_path),
            tofile=os.path.basename(config2_path)
        )
        return "".join(diff)

    def restore_config(self, device_name, backup_file):
        """Restore configuration to a device (simplistic approach)."""
        with open(backup_file, 'r') as f:
            commands = f.read().splitlines()
            
        logger.warning(f"Restoring config for {device_name} from {backup_file}")
        return self.dm.push_config(device_name, commands)

    def compliance_check(self, device_name, template_path):
        """Check if device configuration matches a policy template."""
        import re
        running_config = self.dm.get_config(device_name)
        
        with open(template_path, 'r') as f:
            required_commands = f.read().splitlines()
            
        missing_commands = []
        for cmd in required_commands:
            if not cmd.strip():
                continue
            if not re.search(re.escape(cmd.strip()), running_config):
                missing_commands.append(cmd)
                
        return missing_commands
