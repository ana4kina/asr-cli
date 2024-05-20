from abc import ABC, abstractmethod
from typing import List

import torch

from asr_cli.vad.data_classes import WindowBound


class VAD(ABC):

    @abstractmethod
    def process(self, audio: torch.Tensor) -> List[WindowBound]:
        """
        Main speech recognition process method
        Args:
            audio: 1-channal audio
        Returns:
            List of audio windows
        """
        pass
