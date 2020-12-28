# Enable recursive typing for python 3.7+ (from 3.10 it is build-in)
from __future__ import annotations

from time import time


class BoardInfo:

    def __init__(self):
        self.timestamp: float = time()
        self.model: str = "unknown"
        self.adc: str = "integrated"
        self.resolution: int = 0        # bits
        self.frequency: float = 0.0
        self.num_samples: int = 0           # counter
        self.num_channels: int = 0
        self.sample_time: float = 0.0
        self.v_ref: int = 0             # mV
        self.uid: int = 0
        self.ip: str = ""

    def is_timeout(self, timeout: float) -> bool:
        if self.timestamp - time() > timeout and not __debug__:
            return True
        return False

    def __eq__(self, other: BoardInfo) -> bool:
        return self.model == other.model \
               and self.adc == other.adc \
               and self.resolution == other.resolution \
               and self.frequency == other.frequency \
               and self.num_samples == other.num_samples \
               and self.num_channels == other.num_channels \
               and self.sample_time == other.sample_time \
               and self.v_ref == other.v_ref \
               and self.uid == other.uid \
               and self.ip == other.ip

    def __str__(self) -> str:
        return self.model + " (" + hex(self.uid) + ")"
