# halo-test-environment

[![Build Status](https://travis-ci.org/cloudpassage/halo-test-environment.svg?branch=master)](https://travis-ci.org/cloudpassage/halo-test-environment)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ece9d8ccf9c487fcc9e1/test_coverage)](https://codeclimate.com/github/cloudpassage/halo-test-environment/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/ece9d8ccf9c487fcc9e1/maintainability)](https://codeclimate.com/github/cloudpassage/halo-test-environment/maintainability)

**This is not an officially-supported CloudPassage tool. Use at your own risk!**

Use CloudFormation to quickly instantiate Halo-registered workloads.

This tool will provision and de-provision Linux EC2 instances (up to 10) in a
new VPC, in your region of choice.

## Environment Variables

These environment variables are required for operation:

| Variable Name         | Purpose                                            |
|-----------------------|----------------------------------------------------|
| AWS_ACCESS_KEY_ID     | AWS API key.                                       |
| AWS_SECRET_ACCESS_KEY | AWS API secret.                                    |
| AWS_SSH_KEY_NAME      | Name of SSH key to be installed in EC2 instance.   |
| AWS_REGION            | Region for EC2 instantiation.                      |
| AMI_ID                | ID of AMI to instantiate.                          |
| CLI_CMD               | Base-64 encoded script to run on boot. (optional)  |
| HALO_AGENT_KEY        | Halo agent registration key.                       |
| ENVIRONMENT_NAME      | Name of environment. Must be unique.               |
| HALO_GROUP_TAG        | Halo group provisioning tag. Defaults to `test`.   |
| SERVER_COUNT          | How many instances? Optional. Default 1, Max 10.   |


## Building

docker build -t halo-test-environment .

## Use

### Provisioning Workloads

```shell
    docker run -it --rm \
    -e "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" \
    -e "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" \
    -e "AWS_SSH_KEY_NAME=${AWS_SSH_KEY_NAME}" \
    -e "AWS_REGION=${AWS_REGION}" \
    -e "AMI_ID=${AMI_ID}" \
    -e "CLI_CMD=${CLI_CMD}" \
    -e "HALO_AGENT_KEY=${HALO_AGENT_KEY}" \
    -e "ENVIRONMENT_NAME=${ENVIRONMENT_NAME}" \
    -e "HALO_GROUP_TAG=${HALO_GROUP_TAG}" \
    -e "SERVER_COUNT=${SERVER_COUNT}" \
    halo-test-environment \
    build
```

A non-zero exit indicates that instance instantiation failed.


### Deprovisioning workloads

```shell
    docker run -it --rm \
    -e "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" \
    -e "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" \
    -e "ENVIRONMENT_NAME=${ENVIRONMENT_NAME}"
    halo-test-environment \
    deprovision
```
