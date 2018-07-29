import boto3
import os
import sys
import time


class CloudFormation(object):
    def __init__(self, dyn_config):
        self.config = dyn_config
        self.this_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = os.path.join(self.this_file_dir,
                                         "../cloudformation-templates")
        self.provision_template = os.path.join(self.template_dir,
                                               "default.json")

    def provision(self):
        """Wrap the stack provisioning process."""
        config = {}
        config["environment_name"] = self.config.environment_name
        config["aws_key"] = self.config.aws_key
        config["aws_secret"] = self.config.aws_secret
        config["aws_region"] = self.config.aws_region
        config["ssh_key_name"] = self.config.ssh_key_name
        config["halo_agent_key"] = self.config.halo_agent_key
        config["halo_group_tag"] = self.config.halo_group_tag
        config["ami_id"] = self.config.ami_id
        config["server_count"] = self.config.server_count
        template = CloudFormation.load_template_file(self.provision_template)
        CloudFormation.create_stack(template, config)

    def deprovision(self):
        """Wrap the stack deprovisioning process."""
        config = {}
        config["aws_key"] = self.config.aws_key
        config["aws_secret"] = self.config.aws_secret
        config["aws_region"] = self.config.aws_region
        CloudFormation.teardown_stack(config, self.config.environment_name)

    @classmethod
    def load_template_file(cls, template_file):
        with open(template_file, "r") as t_file:
            template = t_file.read()
        return template

    @classmethod
    def create_stack(cls, template, config):
        success = True
        msg = ""
        status = "INCOMPLETE"
        bad_stats = ['CREATE_FAILED', 'ROLLBACK_IN_PROGRESS',
                     'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE',
                     'DELETE_IN_PROGRESS', 'DELETE_COMPLETE']
        parameters = [
                {'ParameterKey': 'KeyName',
                 'ParameterValue': str(config["ssh_key_name"])},
                {'ParameterKey': 'HaloAgentKey',
                 'ParameterValue': str(config["halo_agent_key"])},
                {'ParameterKey': 'HaloServerTag',
                 'ParameterValue': str(config["halo_group_tag"])},
                {'ParameterKey': 'ServerAMI',
                 'ParameterValue': str(config["ami_id"])},
                {'ParameterKey': 'ServerCount',
                 'ParameterValue': str(config["server_count"])}, ]
        session = CloudFormation.create_session(config["aws_key"],
                                                config["aws_secret"],
                                                config["aws_region"])
        client = session.client('cloudformation')
        response = client.create_stack(StackName=config["environment_name"],
                                       TemplateBody=template,
                                       Parameters=parameters,
                                       Capabilities=["CAPABILITY_IAM"])
        stack_id = response['StackId']
        print("Waiting for creation job to complete...")
        while status != 'CREATE_COMPLETE':
            time.sleep(10)
            response = client.describe_stacks(StackName=stack_id)
            status = response["Stacks"][0]["StackStatus"]
            if status in bad_stats:
                print("Uh oh, something's wrong...", status)
                success = False
                msg = status
                sys.exit(2)
            print("Current status: " + str(status))
        return(success, msg, stack_id)

    @classmethod
    def teardown_stack(cls, config, stack_id):
        success = True
        msg = ""
        session = CloudFormation.create_session(config["aws_key"],
                                                config["aws_secret"],
                                                config["aws_region"])
        client = session.client('cloudformation')
        client.delete_stack(StackName=stack_id)
        print("Please wait for deletion to complete...")
        while True:
            time.sleep(10)
            response = client.describe_stacks()
            exists, status = CloudFormation.get_stack_status(stack_id,
                                                             response)
            if exists is False:
                break
            print("Current status: " + str(status))
        print("Stack no longer exists, deletion job complete.")
        return(success, msg)

    @classmethod
    def get_stack_status(cls, stack_id, response):
        """Return stack existence and status information."""
        stack_exists = False
        stack_status = "NON-EXISTENT"
        stacks = response["Stacks"]
        if stacks != []:
            for stack in stacks:
                if stack["StackName"] == stack_id:
                    stack_exists = True
                    stack_status = stack["StackStatus"]
                    break
        return(stack_exists, stack_status)

    @classmethod
    def create_session(cls, key, secret, region):
        """Return AWS session object."""
        aws_key = key
        aws_secret = secret
        aws_region = region
        session = boto3.Session(aws_access_key_id=aws_key,
                                aws_secret_access_key=aws_secret,
                                region_name=aws_region)
        return(session)
