"""Unit tests for config_manager.py"""

import imp
import os
import sys

module_name = 'provisioner'

here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)

provisioner = imp.load_module(module_name, fp, pathname, description)


class TestConfigManager:
    def set_monkeypatch_env(self, monkeypatch):
        monkeypatch.setenv('HALO_KEY', 'YELLOW')
        monkeypatch.setenv('HALO_SECRET', 'BLUE')
        monkeypatch.setenv('AWS_KEY', 'GREEN')
        monkeypatch.setenv('AWS_SECRET', 'YELLOW')
        monkeypatch.setenv('AWS_SSH_KEY_NAME', 'ORANGE')
        monkeypatch.setenv('HALO_AGENT_KEY', 'RED')
        monkeypatch.setenv('ENVIRONMENT_NAME', 'VIOLET')

    def set_monkeypatch_bad_env(self, monkeypatch):
        monkeypatch.setenv('HALO_SECRET', 'UNDEFINED')
        monkeypatch.setenv('HALO_SECRET', 'BLUE')
        monkeypatch.setenv('AWS_KEY', 'GREEN')
        monkeypatch.setenv('AWS_SECRET', 'YELLOW')

    def test_config_manager_instantiation(self, monkeypatch):
        self.set_monkeypatch_env(monkeypatch)
        confman = provisioner.ConfigManager()
        assert confman

    def test_config_manager_defaults(self, monkeypatch):
        self.set_monkeypatch_env(monkeypatch)
        confman = provisioner.ConfigManager()
        assert confman.halo_key == 'YELLOW'
        assert confman.halo_secret == 'BLUE'
        assert confman.aws_key == 'GREEN'
        assert confman.aws_secret == 'YELLOW'
