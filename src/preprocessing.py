from typing import List
from asr_cli.vad.vad import VAD
from asr_cli.utils.audio import read_audio
from asr_cli.vad.data_classes import WindowBound
from asr_cli.vad_config import VadArch
from asr_cli.vad_getter import get_vad
import librosa
import numpy as np
import matplotlib.pyplot as plt


FRAME_SIZE = 2048
HOP_SIZE = 512
SAMPLE_RATE = 16_000


def vad(
    wav_path: str,
    vad_cutter: VAD,
) -> str:
    samples, _ = read_audio(wav_path, sampling_rate=SAMPLE_RATE)
    window_bounds: List[WindowBound] = vad_cutter.process(samples)
    print(f'Audio cutted into {len(window_bounds)} windows by VAD')
    samples_segments = []
    for window_bound in window_bounds:
        samples_segments.append(
            samples[window_bound.start_sample:window_bound.end_sample]
        )
    return samples_segments


def preprocess_audio(audio_path: str):
    vad_cutter = get_vad(VadArch.webrtc)
    samples_segments = vad(audio_path, vad_cutter)
    melspectograms = []
    for sample_segment in samples_segments:
        stft_values = np.abs(librosa.stft(
            sample_segment.cpu().detach().numpy(),
            win_length=FRAME_SIZE,
            hop_length=HOP_SIZE))**2
        melspectograms.append(librosa.feature.melspectrogram(S=stft_values, sr=SAMPLE_RATE))
    return melspectograms


def visualize(S, sr, idx):
    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                            y_axis='mel', sr=sr,
                            fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    fig.savefig(f'spectrograms/melspectogram-{idx}.png')
