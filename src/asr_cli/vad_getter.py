from asr_cli.vad_config import VadArch, webrtc_vad_config
from asr_cli.vad.vad_webrtc import WebRTCVAD
from asr_cli.vad.vad import VAD


def get_vad(vad_type: VadArch) -> VAD:
    if vad_type == VadArch.webrtc:
        return WebRTCVAD(webrtc_vad_config)
    else:
        raise ValueError(f"Unknown vad arch: {vad_type=}")
