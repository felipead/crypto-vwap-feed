FROM crypto-vwap-feed/base:latest

RUN set -eux; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        supervisor \
    ; \
# Clean-up
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /tmp/* /var/tmp/*

COPY build/app/supervisor/app.conf /etc/supervisor/app.conf

COPY --chown=app:app build/app/entrypoint.sh /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh


USER app
WORKDIR /home/app

RUN set -eux; \
    pipenv install --system --deploy; \
    pipenv check --system

COPY --chown=app:app src/application /home/app/application

EXPOSE 80

ENTRYPOINT ["/home/app/entrypoint.sh"]
