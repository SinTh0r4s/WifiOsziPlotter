from Headers import BeaconHeader
from time import time


class BoardInfo:

    def __init__(self, beacon: BeaconHeader = None):
        self.timestamp: float = time()
        if beacon is None:
            self.model: str = "unknown"
            self.adc: str = "integrated"
            self.resolution: int = 0        # bits
            self.frequency: float = 0.0
            self.frequency_unit: str = "Hz"
            self.samples: int = 0           # counter
            self.sample_time: float = 0.0
            self.sample_time_unit: str = "sec"
            self.v_ref: int = 0             # mV
            self.uid: int = 0
            self.ip: str = ""
        else:
            self.model: str = beacon.model
            self.adc: str = beacon.adc
            self.resolution: int = beacon.resolution
            if beacon.frequency < 1000:
                self.frequency = beacon.frequency
                self.frequency_unit = "Hz"
            elif beacon.frequency < 1000000:
                self.frequency = beacon.frequency / 1000
                self.frequency_unit = "kHz"
            elif beacon.frequency < 1000000000:
                self.frequency = beacon.frequency / 1000000
                self.frequency_unit = "MHz"
            else:
                self.frequency = beacon.frequency / 1000000000
                self.frequency_unit = "GHz"
            self.samples = beacon.num_samples
            if beacon.sample_time > 1.0:
                self.sample_time = beacon.sample_time
                self.sample_time_unit = "s"
            elif beacon.sample_time > 0.001:
                self.sample_time = beacon.sample_time * 1000
                self.sample_time_unit = "ms"
            elif beacon.sample_time > 0.000001:
                self.sample_time = beacon.sample_time * 1000000
                self.sample_time_unit = "µs"
            else:
                self.sample_time = beacon.sample_time * 1000000000
                self.sample_time_unit = "ns"
            self.v_ref = beacon.v_ref
            self.uid = beacon.uid
            self.ip = beacon.address

    def is_timeout(self) -> bool:
        if self.timestamp - time() > 3:
            return True
        return False
