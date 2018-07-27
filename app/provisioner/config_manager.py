"""Configuration helper class.  Holds all config things."""

import os


class ConfigManager(object):
    """This class is used to manage all configuration information for the
    provisioner module.  It will attempt to determine info from environment
    variables.

    """
    def __init__(self):
        self.aws_key = ConfigManager.get_from_env("AWS_ACCESS_KEY_ID")
        self.aws_secret = ConfigManager.get_from_env("AWS_SECRET_ACCESS_KEY")
        self.aws_key_name = ConfigManager.get_from_env("AWS_SSH_KEY_NAME")
        self.aws_region = ConfigManager.get_from_env("AWS_REGION")
        self.ami_id = ConfigManager.get_from_env("AMI_ID")
        self.cli_cmd = ConfigManager.get_from_env("CLI_CMD")
        self.halo_agent_key = ConfigManager.get_from_env("HALO_AGENT_KEY")
        self.halo_group_tag = ConfigManager.get_from_env("HALO_GROUP_TAG")
        self.server_count = ConfigManager.get_from_env("SERVER_COUNT")
        self.env_name = ConfigManager.get_from_env("ENVIRONMENT_NAME")
        self.vars_are_set = self.all_vars_are_set()
        if self.vars_are_set is False:
            print "DANGER!  Not all config items are set!!"

    @classmethod
    def get_from_env(cls, envvar):
        envvar = os.getenv(envvar, "UNDEFINED")
        return envvar

    def all_vars_are_set(self):
        for env in [self.aws_key,
                    self.aws_secret,
                    self.aws_key_name,
                    self.halo_agent_key,
                    self.env_name,
                    self.aws_region]:
            if env == "UNDEFINED":
                return False
            else:
                return True
