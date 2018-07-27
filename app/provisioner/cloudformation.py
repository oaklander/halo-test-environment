import boto3
import os
import sys
import time


class CloudFormation(object):
    def __init__(self, dyn_config):
        self.env_name = dyn_config.env_name
        self.aws_key = dyn_config.aws_key
        self.aws_secret = dyn_config.aws_secret
        self.aws_region = dyn_config.aws_region
        self.ssh_key_name = dyn_config.aws_key_name
        self.halo_agent_key = dyn_config.halo_agent_key
        self.halo_group_tag = dyn_config.halo_group_tag
        self.ami_id = dyn_config.ami_id
        self.server_count = dyn_config.server_count
        self.this_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_dir = os.path.join(self.this_file_dir,
                                         "../cloudformation-templates")
        self.provision_template = os.path.join(self.template_dir,
                                               "default.json")
        self.augment_template = os.path.join(self.template_dir, "default.json")

    def provision(self):
        config = {}
        config["env_name"] = self.env_name
        config["aws_key"] = self.aws_key
        config["aws_secret"] = self.aws_secret
        config["aws_region"] = self.aws_region
        config["ssh_key_name"] = self.ssh_key_name
        config["halo_agent_key"] = self.halo_agent_key
        config["halo_group_tag"] = self.halo_group_tag
        config["ami_id"] = self.ami_id
        config["server_count"] = self.server_count
        template = CloudFormation.load_template_file(self.provision_template)
        CloudFormation.create_stack(template, config)

    def deprovision(self):
        config = {}
        config["aws_key"] = self.aws_key
        config["aws_secret"] = self.aws_secret
        config["aws_region"] = self.aws_region
        CloudFormation.teardown_stack(config, self.env_name)

    @classmethod
    def load_template_file(cls, template_file):
        with open(template_file, "r") as t_file:
            template = t_file.read()
        return template

    @classmethod
    def create_stack(cls, template, config):
        success = True
        msg = ""
        env_name = config["env_name"]
        az_key = config["aws_key"]
        secret = config["aws_secret"]
        region = config["aws_region"]
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
        session = CloudFormation.create_session(az_key, secret, region)
        client = session.client('cloudformation')
        response = client.create_stack(StackName=env_name,
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
        az_key = config["aws_key"]
        secret = config["aws_secret"]
        region = config["aws_region"]
        session = CloudFormation.create_session(az_key, secret, region)
        client = session.client('cloudformation')
        response = client.delete_stack(StackName=stack_id)
        print("Please wait for deletion job to complete...")
        while True:
            time.sleep(10)
            response = client.describe_stacks()
            stack_exists, stack_status = CloudFormation.get_stack_status(stack_id,
                                                                         response)
            if stack_exists is False:
                break
            print("Current status: " + str(stack_status))
        print("Stack no longer exists, deletion job complete.")
        return(success, msg)

    @classmethod
    def get_stack_status(cls, stack_id, response):
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
        aws_key = key
        aws_secret = secret
        aws_region = region
        session = boto3.Session(aws_access_key_id=aws_key,
                                aws_secret_access_key=aws_secret,
                                region_name=aws_region)
        return(session)
