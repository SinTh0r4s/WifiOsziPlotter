import numpy as np
from time import time
from typing import Dict


class PlotInfo:

    def __init__(self):
        self.timestamp = time()
        self.channels: Dict[int, np.ndarray] = {}
        self.v_ref: int = 3300
        self.resolution: int = 0
        self.frequency: int = 0
        self.board_uid: int = 0
        self.num_samples: int = 0
