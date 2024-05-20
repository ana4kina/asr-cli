from dataclasses import dataclass
from typing import List

import torch
import webrtcvad

from asr_cli.utils.audio_format import float_to_byte
from asr_cli.vad.data_classes import WindowBound
from asr_cli.vad_config import VadConfig
from asr_cli.vad.vad import VAD


@dataclass
class Timestamp:
    start: int
    stop: int


class Cutter:
    def __init__(
        self,
        vad_hop: int,
        max_sec: float,
        min_sec: float,
        sample_rate: int,
        thres: float,
        smoothing: float,
    ):
        self.vad_hop = vad_hop
        self.max_sec = max_sec
        self.min_sec = min_sec
        self.sample_rate = sample_rate
        self.thres = thres
        self.smoothing = smoothing

    def slicer(self, vad_labels: List[int]) -> List[WindowBound]:
        l_hop = 0
        r_hop = 0
        output = []

        for vad_label in vad_labels:
            if vad_label == 1:
                max_cond = (
                    r_hop - l_hop
                ) * self.vad_hop >= self.max_sec * self.sample_rate
                if max_cond:
                    output.append(
                        WindowBound(
                            start_sample=l_hop * self.vad_hop,
                            end_sample=r_hop * self.vad_hop,
                        )
                    )
                    l_hop = r_hop + 1
            else:
                short_cond = (
                    r_hop - l_hop
                ) * self.vad_hop >= self.min_sec * self.sample_rate
                if short_cond:
                    output.append(
                        WindowBound(
                            start_sample=l_hop * self.vad_hop,
                            end_sample=r_hop * self.vad_hop,
                        )
                    )
                l_hop = r_hop + 1
            r_hop += 1

        if (r_hop - l_hop) * self.vad_hop >= self.min_sec * self.sample_rate:
            output.append(
                WindowBound(
                    start_sample=l_hop * self.vad_hop,
                    end_sample=r_hop * self.vad_hop,
                )
            )

        return output

    def label_smoother(self, vad_preds: List[List[float]]) -> List[int]:
        vad_labels = [1 if pred[1] > self.thres else 0 for pred in vad_preds]
        smoothed_labels = self.left_smoothing(vad_labels)
        smoothed_labels.reverse()
        smoothed_labels = self.left_smoothing(smoothed_labels)
        smoothed_labels.reverse()
        return smoothed_labels

    def left_smoothing(self, vad_labels: List[int]) -> List[int]:
        smoothed = [0] * len(vad_labels)
        smoothed_frames = int(self.smoothing // self.vad_hop)
        smoothing_window = smoothed_frames + 1

        if smoothed_frames == 0:
            return vad_labels

        smoothed_sum = sum(vad_labels[:smoothing_window])
        smoothed[0] = 1 if smoothed_sum > 0 else 0

        for i in range(smoothing_window, len(vad_labels)):
            smoothed_sum += vad_labels[i] - vad_labels[i - smoothing_window]
            smoothed[i - smoothing_window + 1] = 1 if smoothed_sum > 0 else 0

        for i in range(len(vad_labels), len(vad_labels) + smoothing_window):
            smoothed_sum -= (
                vad_labels[i - smoothing_window] if i - smoothing_window >= 0 else 0
            )
            if i - smoothing_window < len(smoothed):
                smoothed[i - smoothing_window] = 1 if smoothed_sum > 0 else 0

        return smoothed


class WebRTCVAD(VAD):
    def __init__(self, vad_config: VadConfig):
        self.vad = webrtcvad.Vad(vad_config.vad_mode)
        self.sample_rate = vad_config.sr
        self.min_required_samples = vad_config.min_required_samples
        self.cutter = Cutter(
            vad_hop=vad_config.vad_hop,
            max_sec=vad_config.max_sec,
            min_sec=vad_config.min_sec,
            sample_rate=self.sample_rate,
            thres=vad_config.thres,
            smoothing=vad_config.smoothing,
        )

    def process(self, wav: torch.Tensor) -> List[WindowBound]:

        pcm_data: bytes = float_to_byte(wav)
        vad_events = []
        for frame_bytes in self.frame_generator(pcm_data):
            is_speech = self.vad.is_speech(frame_bytes, self.sample_rate)
            if is_speech:
                vad_events.append([0, 1])
            else:
                vad_events.append([1, 0])

        vad_labels = self.cutter.label_smoother(vad_events)
        windows_bounds = self.cutter.slicer(vad_labels)

        return windows_bounds

    def frame_generator(self, audio: bytes):
        """
        Yields audio bytes frames
        Args:
            audio: full audio PCM16 bytes
        Returns:

        """
        n = 2 * self.min_required_samples
        offset = 0
        timestamp = 0.0
        duration = n / self.sample_rate
        while offset + n <= len(audio):
            yield audio[offset : offset + n]
            timestamp += duration
            offset += n
