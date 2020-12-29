import numpy as np
from time import time
from typing import Dict


class PlotInfo:

    def __init__(self) -> None:
        self.timestamp = time()
        self.channels: Dict[int, np.ndarray] = {}
        self.v_ref: int = 3300
        self.resolution: int = 0
        self.frequency: int = 0
        self.board_uid: int = 0
        self.num_samples: int = 0

    # scipy.io.savemat cannot resolve recursive dictionaries so the data is packed into a list
    def to_dict(self) -> Dict:
        return {"timestamp": self.timestamp, "v_ref": self.v_ref, "resolution": self.resolution,
                "frequency": self.frequency, "board_uid": self.board_uid, "num_samples": self.num_samples,
                "channels": list(self.channels.keys()), "data": list(self.channels.values())}
