"""Configuration helper class.  Holds all config things."""
import os


class ConfigManager(object):
    """Instantiate with ``provision`` or ``deprovision`` as the only argument.

    This class manages the configuration for the application, and verifies that
    all required configuration irems are correctly set.
    """
    required_provision = [("aws_key", "AWS_ACCESS_KEY_ID"),
                          ("aws_secret", "AWS_SECRET_ACCESS_KEY"),
                          ("ssh_key_name", "AWS_SSH_KEY_NAME"),
                          ("aws_region", "AWS_REGION"),
                          ("ami_id", "AMI_ID"),
                          ("halo_agent_key", "HALO_AGENT_KEY"),
                          ("environment_name", "ENVIRONMENT_NAME")]

    optional_provision = [("cli_cmd", "CLI_CMD", ""),
                          ("halo_group_tag", "HALO_GROUP_TAG", "test"),
                          ("server_count", "SERVER_COUNT", "1")]

    required_deprovision = [("aws_key", "AWS_ACCESS_KEY_ID"),
                            ("aws_secret", "AWS_SECRET_ACCESS_KEY"),
                            ("aws_region", "AWS_REGION"),
                            ("environment_name", "ENVIRONMENT_NAME")]

    def __init__(self, operating_mode):
        self.operating_mode = operating_mode
        self.set_operating_vars(operating_mode)

    def set_operating_vars(self, operating_mode):
        """Wrap the process of setting and verifying operating params."""
        if operating_mode == 'provision':
            self.set_required(self.required_provision)
            self.set_optional(self.optional_provision)
        elif operating_mode == 'deprovision':
            self.set_required(self.required_deprovision)
        else:
            raise ValueError("Unsupported operating mode %s" % operating_mode)

    def set_required(self, var_tuples):
        """Set instance variables based on environment variables."""
        missing_vars = []
        for instance_var, env_var in var_tuples:
            from_env = os.getenv(env_var)
            if from_env is None:
                missing_vars.append(env_var)
            else:
                setattr(self, instance_var, from_env)
        if missing_vars:
            msg = "Missing environment variables: %s" % ", ".join(missing_vars)
            raise ValueError(msg)

    def set_optional(self, var_tuples):
        """Set instance variables from environment variables, or defaults."""
        for instance_var, env_var, default in var_tuples:
            setattr(self, instance_var, os.getenv(env_var, default))
