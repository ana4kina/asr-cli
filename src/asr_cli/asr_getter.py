import os
import subprocess
from omegaconf import OmegaConf
from asr_cli.asr.asr import ASR
from asr_cli.asr.asr_gigaam_ctc import GigaAMCTCASR
from asr_cli.asr.asr_wav2vec2_ctc import Wav2Vec2CTCASR
from asr_cli.asr_config import ASRArch, Wav2Vec2CTCConfig, Wav2Vec2CTCRemoteConfig, GigaAMCTCConfig


def download_resources(url, destination):
    try:
        subprocess.run(['wget', url, '-O', destination], check=True)
        print(f"Model downloaded successfully to {destination}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download model: {e}")


def get_asr(asr_arch: ASRArch, remote: bool = False) -> ASR:
    if asr_arch == ASRArch.wav2vec2ctc:
        config = Wav2Vec2CTCRemoteConfig if remote else Wav2Vec2CTCConfig
        return Wav2Vec2CTCASR(config)
    elif asr_arch == ASRArch.gigaam_ctc:
        if not os.path.exists(GigaAMCTCConfig.model_path):
            os.makedirs(os.path.dirname(GigaAMCTCConfig.model_path), exist_ok=True)
            model_url = 'https://n-ws-q0bez.s3pd12.sbercloud.ru/b-ws-q0bez-jpv/GigaAM/ctc_model_weights.ckpt'
            download_resources(model_url, GigaAMCTCConfig.model_path)
        else:
            print(f"Model already exists at {GigaAMCTCConfig.model_path}")

        if not os.path.exists(GigaAMCTCConfig.config_path):
            os.makedirs(os.path.dirname(GigaAMCTCConfig.config_path), exist_ok=True)
            config_url = 'https://n-ws-q0bez.s3pd12.sbercloud.ru/b-ws-q0bez-jpv/GigaAM/ctc_model_config.yaml'
            download_resources(config_url, GigaAMCTCConfig.config_path)
        else:
            print(f"Config already exists at {GigaAMCTCConfig.config_path}")

        conf = OmegaConf.load(GigaAMCTCConfig.config_path)
        conf_current_preprocessor = conf["preprocessor"]["_target_"]
        conf_current_module, conf_processor = conf_current_preprocessor.rsplit(".", 1)
        if conf_current_module != "asr_cli.asr.asr_gigaam_ctc":
            conf_target_preprocessor = ".".join(["asr_cli.asr.asr_gigaam_ctc", conf_processor])
            conf["preprocessor"]["_target_"] = conf_target_preprocessor
            OmegaConf.save(conf, GigaAMCTCConfig.config_path)
        return GigaAMCTCASR(GigaAMCTCConfig)
    else:
        raise ValueError(f"Unknown {asr_arch=}")
