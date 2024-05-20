from typing import List
import tempfile
import warnings
warnings.filterwarnings("ignore")

import torch
import torchaudio
from nemo.collections.asr.models import EncDecCTCModel
from nemo.collections.asr.modules.audio_preprocessing import (
    AudioToMelSpectrogramPreprocessor as NeMoAudioToMelSpectrogramPreprocessor,
)
from nemo.collections.asr.parts.preprocessing.features import (
    FilterbankFeaturesTA as NeMoFilterbankFeaturesTA,
)
from asr_cli.utils.audio import save_audio
from asr_cli.asr_config import ASRConfig
from asr_cli.asr.asr import ASR


class FilterbankFeaturesTA(NeMoFilterbankFeaturesTA):
    def __init__(self, mel_scale: str = "htk", wkwargs=None, **kwargs):
        if "window_size" in kwargs:
            del kwargs["window_size"]
        if "window_stride" in kwargs:
            del kwargs["window_stride"]

        super().__init__(**kwargs)

        self._mel_spec_extractor = torchaudio.transforms.MelSpectrogram(
            sample_rate=self._sample_rate,
            win_length=self.win_length,
            hop_length=self.hop_length,
            n_mels=kwargs["nfilt"],
            window_fn=self.torch_windows[kwargs["window"]],
            mel_scale=mel_scale,
            norm=kwargs["mel_norm"],
            n_fft=kwargs["n_fft"],
            f_max=kwargs.get("highfreq", None),
            f_min=kwargs.get("lowfreq", 0),
            wkwargs=wkwargs,
        )


class AudioToMelSpectrogramPreprocessor(NeMoAudioToMelSpectrogramPreprocessor):
    def __init__(self, mel_scale: str = "htk", **kwargs):
        super().__init__(**kwargs)
        kwargs["nfilt"] = kwargs["features"]
        del kwargs["features"]
        self.featurizer = FilterbankFeaturesTA(  # Deprecated arguments; kept for config compatibility
            mel_scale=mel_scale, **kwargs,
        )

class GigaAMCTCASR(ASR):
    def __init__(self, asr_config: ASRConfig) -> None:
        self.model = EncDecCTCModel.from_config_file(asr_config.config_path)
        ckpt = torch.load(asr_config.model_path, map_location="cpu")
        self.model.load_state_dict(ckpt, strict=False)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.model = self.model.to(device)
        self.model.eval()

    def recognize(self, audio: torch.Tensor) -> str:
        with tempfile.NamedTemporaryFile() as tmp_wav_fout:
            tmp_wav_path = tmp_wav_fout.name + ".wav"
            save_audio(tmp_wav_path, audio, sampling_rate=16_000)
            transcription = self.model.transcribe([tmp_wav_path])[0]
        return transcription

    def process(self, segments: List[torch.Tensor]) -> torch.List[str]:
        results = []
        # doing batch_size=1 for now
        for audio in segments:
            results.append(self.recognize(audio))

        return results
