class BoardInfo:

    def __init__(self):
        self.model: str = "unknown"
        self.adc: str = "integrated"
        self.resolution: int = 0        # bits
        self.frequency: float = 0.0
        self.frequency_unit: str = "Hz"
        self.samples: int = 0           # counter
        self.sample_time: float = 0.0
        self.sample_time_unit: str = "sec"
        self.v_ref: int = 0             # mV
