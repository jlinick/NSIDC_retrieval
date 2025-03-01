#!/bin/bash

# builds and jumps into a running container to run NSIDC retrieval scripts

# Docker image name and tag
REPO='nsidc'
TAG='0.0.1'

# Detect OS and set local paths
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS - Use the current username dynamically
  USERNAME=$(whoami)
  LOCAL_PRODUCT_DIR="/Users/${USERNAME}/products/${REPO}"
  LOCAL_DATA_DIR="/Users/${USERNAME}/data/${REPO}"
else
  # Linux (default)
  LOCAL_PRODUCT_DIR="/home/jlinick/products/${REPO}"
  LOCAL_DATA_DIR="/home/jlinick/data/${REPO}"
fi

# Ensure directories exist
if [[ ! -d "$LOCAL_PRODUCT_DIR" ]]; then
  echo "Error: Directory '$LOCAL_PRODUCT_DIR' does not exist." >&2
  exit 1
fi

if [[ ! -d "$LOCAL_DATA_DIR" ]]; then
  echo "Error: Directory '$LOCAL_DATA_DIR' does not exist." >&2
  exit 1
fi

# Paths inside the Docker container
DOCKER_PRODUCT_DIR='/products'
DOCKER_DATA_DIR='/data'
DOCKER_CODE_DIR='/code'
DOCKER_IMAGE="${REPO}"
DOCKER_TAG="${TAG}"

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

build_dockerfile() {
    cd "${SCRIPT_DIR}"
    if [[ "$(docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} 2> /dev/null)" == "" ]]; then
        echo "${DOCKER_IMAGE}:${DOCKER_TAG} does not exist, building..."
        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f ${SCRIPT_DIR}/docker/Dockerfile .
    else
        echo "${DOCKER_IMAGE}:${DOCKER_TAG} exists, starting..."
    fi
}

# Build/check Docker image
build_dockerfile

# Run container
docker run --rm -ti \
    -v ~/.netrc:/root/.netrc:ro \
    -v "${LOCAL_DATA_DIR}:${DOCKER_DATA_DIR}" \
    -v "${SCRIPT_DIR}:${DOCKER_CODE_DIR}" \
    -v "${LOCAL_PRODUCT_DIR}:${DOCKER_PRODUCT_DIR}" \
    "${DOCKER_IMAGE}:${DOCKER_TAG}" \
    /bin/bash
