"""Unit tests for config_manager.py"""
import imp
import os
import pytest
import sys

module_name = 'provisioner'

here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
provisioner = imp.load_module(module_name, fp, pathname, description)


class TestConfigManager:
    def set_monkeypatch_env_provision(self, monkeypatch):
        monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'GREEN')
        monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'YELLOW')
        monkeypatch.setenv('AWS_SSH_KEY_NAME', 'ORANGE')
        monkeypatch.setenv('AWS_REGION', 'ELSEWEYR')
        monkeypatch.setenv('AMI_ID', 'ami-whatever')
        monkeypatch.setenv('HALO_AGENT_KEY', 'RED')
        monkeypatch.setenv('ENVIRONMENT_NAME', 'VIOLET')

    def set_monkeypatch_env_deprovision(self, monkeypatch):
        monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'GREEN')
        monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'YELLOW')
        monkeypatch.setenv('AWS_REGION', 'ELSEWEYR')
        monkeypatch.setenv('ENVIRONMENT_NAME', 'VIOLET')

    def set_monkeypatch_bad_env(self, monkeypatch):
        monkeypatch.setenv('AWS_KEY', 'GREEN')
        monkeypatch.setenv('AWS_SECRET', 'YELLOW')

    def test_config_manager_instantiate_provision(self, monkeypatch):
        self.set_monkeypatch_env_provision(monkeypatch)
        confman = provisioner.ConfigManager('provision')
        assert confman

    def test_config_manager_instantiate_deprovision(self, monkeypatch):
        self.set_monkeypatch_env_deprovision(monkeypatch)
        confman = provisioner.ConfigManager('deprovision')
        assert confman

    def test_config_manager_fail_provision(self, monkeypatch):
        self.set_monkeypatch_bad_env(monkeypatch)
        with pytest.raises(ValueError):
            provisioner.ConfigManager('provision')

    def test_config_manager_fail_deprovision(self, monkeypatch):
        self.set_monkeypatch_bad_env(monkeypatch)
        with pytest.raises(ValueError):
            provisioner.ConfigManager('deprovision')

    def test_config_manager_fail_bad_mode(self, monkeypatch):
        self.set_monkeypatch_bad_env(monkeypatch)
        with pytest.raises(ValueError):
            provisioner.ConfigManager('bad_mode')
