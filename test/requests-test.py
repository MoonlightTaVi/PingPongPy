import unittest

import requests

from pong.core.tools.reboot import RequestReboot
from pong.core.config import ConfigReader


class RequestsTest(unittest.TestCase):
    """Unit tests for the 'requests' module."""
    def test_get_ok(self):
        """A simple test to check that the 'requests' work."""
        response = requests.get("https://www.google.com")
        status = response.status_code
        self.assertEqual(200, status)
    def test_reboot_ok(self):
        cfg = ConfigReader()
        rbt = RequestReboot()
        rbt.load_config(cfg.get_config())
        self.assertTrue(rbt.start())


if __name__ == '__main__':
    unittest.main()