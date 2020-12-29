from osziplotter.network.Headers import SampleTransmissionHeader
from osziplotter.modelcontroller.PlotInfo import PlotInfo
from osziplotter.Util import get_bytes_per_sample

from math import floor
from time import time
import numpy as np


class SampleGroup:

    def __init__(self, header: SampleTransmissionHeader):
        self._samples = [None] * header.num_frames
        self._header = header
        self._bytes_per_sample = get_bytes_per_sample(self._header.resolution)
        self._timestamp_sec: float = time()

    def timeout(self) -> bool:
        if time() - self._timestamp_sec > 2 and not __debug__:
            return True
        return False

    def is_complete(self) -> bool:
        for segment in self._samples:
            if segment is None:
                return False
        return True

    def add_packet(self, header: SampleTransmissionHeader) -> bool:
        if not self._header.same_transmission_group(header):
            return False
        samples_per_channel = self._header.num_samples / self._header.channels
        if samples_per_channel is float:
            print("Fatal error: received data is misaligned")
        samples_per_channel = floor(samples_per_channel)
        channels = [np.zeros(samples_per_channel)] * self._header.channels
        max_value_bits = (1 << header.resolution) - 1
        # noinspection PyPep8Naming
        sample_to_mV = header.v_ref / max_value_bits
        for s in range(samples_per_channel):
            for c in range(header.channels):
                offset = (s * header.channels + c) * self._bytes_per_sample
                value = int.from_bytes(header.payload[offset:offset + self._bytes_per_sample], 'little')
                channels[c][s] = value * sample_to_mV
        self._samples[header.frame_id] = channels
        return True

    def get_samples(self) -> PlotInfo:
        channels = {}
        for i in range(self._header.channels):
            channels[i] = np.zeros(0)
        for segment in self._samples:
            for i in range(self._header.channels):
                channels[i] = np.append(channels[i], segment[i])
        plot = self._header.to_plot_info()
        plot.channels = channels
        return plot
