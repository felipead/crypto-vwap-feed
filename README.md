# Crypto VWAP (Volume-Weighted Average Price) Feed

This is a real-time VWAP ([volume-weighted average price](https://en.wikipedia.org/wiki/Volume-weighted_average_price)) calculation engine.

## Requirements

- `docker` or [Docker Desktop](https://docs.docker.com/desktop/)
- `docker-compose` (included with _Docker Desktop_)

## Setup

This will build the necessary Docker images:

```
./build.sh
```

## Run the test suite

Tests are run by [`pytest`](https://docs.pytest.org/en/stable/) within the CI Docker containers.

```
./test.sh
```

## Run lint (code style checks)

Checks are run by [`Flake8`](https://flake8.pycqa.org/en/latest/) within the CI Docker containers.

```
./lint.sh
```

## Run the application

```
./run.sh
```
