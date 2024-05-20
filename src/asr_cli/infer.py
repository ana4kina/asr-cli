"""
    Simple asr infernece
"""

from typing import List
from asr_cli.asr.asr import ASR
from asr_cli.vad.vad import VAD
from asr_cli.utils.audio import read_audio
from asr_cli.vad.data_classes import WindowBound


def infer(
    wav_path: str,
    asr_recognizer: ASR,
    vad_cutter: VAD,
) -> str:
    samples, _ = read_audio(wav_path, sampling_rate=16_000)
    window_bounds: List[WindowBound] = vad_cutter.process(samples)
    print(f"Audio cutted into {len(window_bounds)} windows by VAD")
    samples_segments = []
    for window_bound in window_bounds:
        # batch_size = 1
        samples_segments.append(
            samples[window_bound.start_sample : window_bound.end_sample]
        )

    asr_results = asr_recognizer.process(segments=samples_segments)

    return " ".join(asr_results)
