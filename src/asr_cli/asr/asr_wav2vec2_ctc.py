from typing import List

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from asr_cli.asr_config import ASRConfig
from asr_cli.asr.asr import ASR


class Wav2Vec2CTCASR(ASR):
    def __init__(self, asr_config: ASRConfig) -> None:
        self.processor = Wav2Vec2Processor.from_pretrained(asr_config.processor_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(asr_config.model_path)
        self.sr = 16_000

    def recognize(self, audio: torch.Tensor) -> str:
        inputs = self.processor(
            audio, sampling_rate=self.sr, return_tensors="pt", padding=True
        )
        with torch.no_grad():
            logits = self.model(
                inputs.input_values, attention_mask=inputs.attention_mask
            ).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentences = self.processor.batch_decode(predicted_ids)
        return predicted_sentences[0]

    def process(self, segments: List[torch.Tensor]) -> torch.List[str]:
        results = []
        # doing batch_size=1 for now
        for audio in segments:
            results.append(self.recognize(audio))

        return results
