#!/usr/bin/env bash
mkdir ./data
wget https://n-ws-q0bez.s3pd12.sbercloud.ru/b-ws-q0bez-jpv/GigaAM/{ssl_model_weights.ckpt,emo_model_weights.ckpt,ctc_model_weights.ckpt,ctc_model_config.yaml,emo_model_config.yaml,encoder_config.yaml,example.mp3} -P ./data
