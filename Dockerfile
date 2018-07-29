FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.6
MAINTAINER toolbox@cloudpassage.com

ARG CC_TEST_REPORTER_ID

RUN apt-get update && apt-get install -y curl git

RUN pip install boto3 colorama pytest pytest-cov

COPY . /src/

WORKDIR /src/app


RUN curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
RUN chmod +x ./cc-test-reporter
RUN ./cc-test-reporter before-build || echo "Not sending test results."

RUN py.test --cov-report term-missing --cov-report xml --cov=provisioner; ./cc-test-reporter after-build -d -t coverage.py --exit-code $? || echo "Not sending test results."

##########

FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.6
MAINTAINER toolbox@cloudpassage.com

RUN pip install boto3 colorama

COPY app /app/

WORKDIR /app

ENTRYPOINT ["/usr/bin/python", "/app/application.py"]

CMD ["-h"]
