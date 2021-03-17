FROM ubuntu:20.04

ENV TZ UTC
ENV LANG C.UTF-8
ENV PYTHONPATH /home/app

RUN groupadd --system app; \
    useradd --no-log-init --system --create-home --gid app app

RUN set -eux; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get upgrade -y -o Dpkg::Options::="--force-confold"; \
    apt-get install -y --no-install-recommends \
# Python
        python3.8 \
        python3-pip \
    ; \
# Sanity test
    python3 --version; \
# Clean-up
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /tmp/* /var/tmp/*

RUN set -eux; \
# Python setup
    ln -s /usr/bin/python3 /usr/bin/python; \
    ln -s /usr/bin/pip3 /usr/bin/pip; \
    pip install pipenv; \
# Sanity test
    python --version; \
    pip --version; \
    pipenv --version

COPY Pipfile /home/app/Pipfile
COPY Pipfile.lock /home/app/Pipfile.lock
