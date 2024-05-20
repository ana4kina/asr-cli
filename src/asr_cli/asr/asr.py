from abc import ABC, abstractmethod
from typing import List

import torch


class ASR(ABC):

    @abstractmethod
    def process(self, segments: List[torch.Tensor]) -> List[str]:
        """
        Main speech recognition process method
        Args:
            segments: list of 1-channal audio windows
        """
        pass
