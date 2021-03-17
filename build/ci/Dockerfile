FROM crypto-vwap-feed/base:latest

# This is where Pipenv install Python tools, such as pytest, flake8 and alembic
ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app build/ci/task.sh /home/app/task.sh
RUN chmod +x /home/app/task.sh

USER app
WORKDIR /home/app

RUN set -eux; \
    pipenv install --system --deploy --dev; \
    pipenv check --system

COPY --chown=app:app src/application /home/app/application
COPY --chown=app:app src/tests /home/app/tests
COPY --chown=app:app .flake8 /home/app/.flake8

ENTRYPOINT ["/home/app/task.sh"]
