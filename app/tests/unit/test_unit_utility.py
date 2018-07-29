"""Unit tests for utility.py"""
import imp
import os
import sys

module_name = 'provisioner'

here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
provisioner = imp.load_module(module_name, fp, pathname, description)
util = provisioner.Utility()


class TestUnitUtility:
    def test_unit_utility_print_error_message(self):
        assert util.print_error_message("ERROR") is None

    def test_unit_utility_print_error_informational(self):
        assert util.print_informational_message("INFORMATIONAL") is None

    def test_unit_utility_print_debug_message(self):
        assert util.print_error_message("DEBUG") is None

    def test_unit_utility_print_halo_status_message(self):
        assert util.print_error_message("HALO STATUS") is None

    def test_unit_utility_print_aws_status_message_message(self):
        assert util.print_error_message("AWS STATUS") is None
