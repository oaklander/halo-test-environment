#!/usr/bin/python
import argparse
import botocore
import provisioner
import sys


def main():
    dyn_config = provisioner.ConfigManager()
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="(provision|deprovision)")
    args = parser.parse_args()
    if args.mode == "provision":
        provision(dyn_config)
    elif args.mode == "deprovision":
        deprovision(dyn_config)
    else:
        msg_str = "Valid modes: 'provision', 'deprovision'"
        msg = provisioner.Utility()
        msg.print_aws_status_message(msg_str)
        sys.exit(3)


def provision(dyn_config):
    print("Starting provisioning.")
    msg = provisioner.Utility()
    try:
        msg.print_aws_status_message("Provisioning AWS resources")
        cloudformation = provisioner.CloudFormation(dyn_config)
        cloudformation.provision()
        msg.print_aws_status_message("AWS provisioning process complete!")
    except botocore.exceptions.ClientError as e:
        msg_str = str(e)
        msg.print_error_message(msg_str)
        sys.exit(1)
    except Exception as e:
        msg_str = str("Error in CloudFormation provisioning process!!!\n" +
                      "    Please run the teardown routine (refer to README.md)\n" +
                      "    or manually de-provision by logging into your AWS account," +
                      " navigating to the CloudFormation module and deleting this stack.\n" +
                      str(e))
        msg.print_error_message(msg_str)
        sys.exit(2)


def deprovision(dyn_config):
    print("Starting deprovisioning.")
    msg = provisioner.Utility()
    try:
        cloudformation = provisioner.CloudFormation(dyn_config)
        status_msg = "De-provisioning AWS stack %s." % cloudformation.env_name
        msg.print_aws_status_message(status_msg)
        cloudformation.deprovision()
    except botocore.exceptions.ClientError as e:
        msg_str = str(e)
        msg.print_error_message(msg_str)
        sys.exit(1)


if __name__ == "__main__":
    main()
