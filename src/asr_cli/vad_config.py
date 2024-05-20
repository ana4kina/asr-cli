import dataclasses
from enum import Enum
from typing import Optional


class VadArch(Enum):
    webrtc = "webrtc"


@dataclasses.dataclass
class VadConfig:
    sr: int
    min_required_samples: Optional[int] = None
    vad_hop: Optional[int] = None
    max_sec: Optional[int] = None
    min_sec: Optional[int] = None
    thres: Optional[int] = None
    smoothing: Optional[int] = None
    vad_mode: Optional[int] = None


webrtc_vad_config = VadConfig(
    sr=16_000,
    min_required_samples=320,
    vad_hop=320,
    max_sec=11.0,
    min_sec=0.5,
    thres=0.6,
    smoothing=640,
    vad_mode=2,
)
