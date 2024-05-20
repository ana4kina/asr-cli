from typing import Tuple

import torch
import torchaudio


def read_audio(
    path: str,
    sampling_rate: int = 16_000,
) -> Tuple[torch.Tensor, int]:
    wav, sr = torchaudio.load(path)
    if wav.size(0) > 1:
        wav = wav.mean(dim=0, keepdim=True)

    if sampling_rate != sr:
        transform = torchaudio.transforms.Resample(orig_freq=sr, new_freq=sampling_rate)
        wav = transform(wav)
        sr = sampling_rate

    return wav.squeeze(0), sr

def save_audio(path: str, tensor: torch.Tensor, sampling_rate: int = 16_000):
    torchaudio.save(
        path,
        tensor.unsqueeze(0),
        sampling_rate,
        bits_per_sample=16,
        format="wav",
        encoding="PCM_S"
    )
