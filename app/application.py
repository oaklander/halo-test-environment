#!/usr/bin/python
import argparse
import botocore
import datetime
import provisioner
import sys


def main():
    start_time = datetime.datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="(provision|deprovision)")
    args = parser.parse_args()
    dyn_config = provisioner.ConfigManager(args.mode)
    if args.mode == "provision":
        provision(dyn_config)
    elif args.mode == "deprovision":
        deprovision(dyn_config)
    else:
        msg_str = "Valid modes: 'provision', 'deprovision'"
        msg = provisioner.Utility()
        msg.print_aws_status_message(msg_str)
        sys.exit(3)
    end_time = datetime.datetime.now()
    print_status(start_time, end_time)


def provision(dyn_config):
    print("Starting provisioning.")
    msg = provisioner.Utility()
    try:
        msg.print_aws_status_message("Provisioning AWS resources")
        cf = provisioner.CloudFormation(dyn_config)
        cf.provision()
        msg.print_aws_status_message("AWS provisioning process complete!")
    except botocore.exceptions.ClientError as e:
        msg_str = str(e)
        msg.print_error_message(msg_str)
        sys.exit(1)
    except Exception as e:
        msg_str = str("Error in CloudFormation provisioning process!!!\n" +
                      "Troubleshoot, deprovision, and try again!\n" +
                      str(e))
        msg.print_error_message(msg_str)
        sys.exit(2)


def deprovision(dyn_config):
    print("Starting deprovisioning.")
    msg = provisioner.Utility()
    try:
        cf = provisioner.CloudFormation(dyn_config)
        stack_name = cf.config.environment_name
        status_msg = "De-provisioning AWS stack %s." % stack_name
        msg.print_aws_status_message(status_msg)
        cf.deprovision()
    except botocore.exceptions.ClientError as e:
        msg_str = str(e)
        msg.print_error_message(msg_str)
        sys.exit(1)


def print_status(start_time, end_time):
    msg = provisioner.Utility()
    delta = end_time - start_time
    msg_lst = ["Start: %s" % start_time.isoformat().split("T")[1],
               "Finish: %s" % end_time.isoformat().split("T")[1],
               "Elapsed: %s seconds." % delta.seconds]
    for msg_str in msg_lst:
        msg.print_informational_message(msg_str)


if __name__ == "__main__":
    main()
