import os
import dataclasses
from enum import Enum
from typing import Optional

resources_path = os.path.join(os.path.dirname(__file__), "resources")


class ASRArch(Enum):
    wav2vec2ctc = "wav2vec2ctc"
    gigaam_ctc = "gigaam_ctc"


@dataclasses.dataclass
class ASRConfig:
    model_path: str
    processor_path: Optional[str] = None
    config_path: Optional[str] = None

# No Wav2Vec2 resources will be included in pypi resources
Wav2Vec2CTCConfig = ASRConfig(
    processor_path=os.path.join(resources_path, "wav2vec2ctc_processor.pt"),
    model_path=os.path.join(resources_path, "wav2vec2ctc.pt"),
)

Wav2Vec2CTCRemoteConfig = ASRConfig(
    processor_path="jonatasgrosman/wav2vec2-large-xlsr-53-russian",
    model_path="jonatasgrosman/wav2vec2-large-xlsr-53-russian",
)

GigaAMCTCConfig = ASRConfig(
    model_path=os.path.join(resources_path, "gigaam_ctc/ctc_model_weights.ckpt"),
    config_path=os.path.join(resources_path, "gigaam_ctc/ctc_model_config.yaml"),
)
