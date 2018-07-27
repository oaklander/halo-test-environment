FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.6
MAINTAINER toolbox@cloudpassage.com

RUN pip install boto3 colorama pytest pytest-cov

COPY app /app/

WORKDIR /app

CMD py.test --cov=builder

##########

FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.0.6
MAINTAINER toolbox@cloudpassage.com

RUN pip install boto3 colorama

COPY app /app/

WORKDIR /app

ENTRYPOINT ["/usr/bin/python", "/app/application.py"]

CMD ["-h"]
