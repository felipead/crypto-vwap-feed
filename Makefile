
CACHE=true

ifeq ($(CACHE),true)
  BUILD_OPTIONS=
else
  BUILD_OPTIONS=--no-cache
endif

DOCKER_BUILD=docker build $(BUILD_OPTIONS)

# ---

ALL_IMAGES = base app ci

.PHONY: $(ALL_IMAGES) clean

all: $(ALL_IMAGES)

# ---

base:
	$(DOCKER_BUILD) -t crypto-vwap-feed/base -f ./build/base.dockerfile .

app: base
	$(DOCKER_BUILD) -t crypto-vwap-feed/app -f ./build/app/Dockerfile .

ci: base
	$(DOCKER_BUILD) -t crypto-vwap-feed/ci -f ./build/ci/Dockerfile .

# ---

clean:
	yes | docker image prune
	yes | docker container prune
