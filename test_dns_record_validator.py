import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import validate


class TestZoneValidator(unittest.TestCase):
    def test_valid_a_record(self):
        self.assertIsNone(validate("www IN A 192.0.2.10"))

    def test_bad_ipv4_flagged(self):
        self.assertIsNotNone(validate("www IN A 999.1.1.1"))

    def test_valid_mx_record(self):
        self.assertIsNone(validate("@ IN MX 10 mail.example.com."))

    def test_unknown_type_flagged(self):
        self.assertIsNotNone(validate("www IN SRV 10 60 80 host."))
