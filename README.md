# asr-cli
Simple ASR CLI tool

## Installation
```
python3 -m pip install Cython
python3 -m pip install -e .
```
## Use as a CLI tool
```
asr-cli --wav_path examples/resources/tts-example.wav
```

## Usage with Docker
```bash
./run.sh # build and run docker container
# Откроется bash в контейнере, далее работаем в нем
cd /_mnt # Переходи в директорию, которую примаунтили к контейнеру на запуске
# Распознаем пример
asr-cli --wav_path examples/resources/tts-example.wav
```
