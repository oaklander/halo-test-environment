"""Unit tests for cloudformation.py"""
import imp
import os
import sys

module_name = 'provisioner'

here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
provisioner = imp.load_module(module_name, fp, pathname, description)


class TestCloudFormation:
    def test_unit_cloudformation_get_stack_status(self):
        stack_id = "abc123"
        response = {"Stacks": [{"StackName": "MyStack",
                                "StackStatus": "There"},
                               {"StackName": "abc123",
                                "StackStatus": "Here"}]}
        exists, status = provisioner.CloudFormation.get_stack_status(stack_id,
                                                                     response)
        assert exists is True
        assert status == "Here"

    def test_unit_cloudformation_get_stack_status_nonexist(self):
        stack_id = "abc1234"
        response = {"Stacks": [{"StackName": "MyStack",
                                "StackStatus": "There"},
                               {"StackName": "abc123",
                                "StackStatus": "Here"}]}
        exists, status = provisioner.CloudFormation.get_stack_status(stack_id,
                                                                     response)
        assert exists is False
        assert status == "NON-EXISTENT"
