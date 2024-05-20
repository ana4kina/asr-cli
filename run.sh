#!/usr/bin/env bash
set -x 
docker rm -f asr-cli-debug

set -e
docker build -t asr-cli:latest -f Dockerfile .
docker run -v $(pwd):/_mnt --name asr-cli-debug -d asr-cli:latest sleep inf
docker exec -it asr-cli-debug bash
