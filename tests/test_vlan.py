import unittest
from unittest.mock import MagicMock
from src.vlan_manager import VLANManager
from src.device_manager import DeviceManager

class TestVLANManager(unittest.TestCase):
    def setUp(self):
        self.dm = DeviceManager()
        self.dm.push_config = MagicMock(return_value="OK")
        self.vlan_mgr = VLANManager(self.dm)

    def test_create_vlan(self):
        self.vlan_mgr.create_vlan("switch-01", 10, "Users")
        self.dm.push_config.assert_called_with("switch-01", ["vlan 10", "name Users"])

if __name__ == '__main__':
    unittest.main()
