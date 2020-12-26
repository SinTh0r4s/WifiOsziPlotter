from typing import List
from Util import get_bytes_per_sample
import struct

magic_number: int = 7567
little_endian: str = "little"
encoding_utf8: str = "utf-8"
ignore_errors: str = "ignore"


class BeaconHeader:

    def __init__(self):
        self.resolution: int = 0
        self.channels: int = 0
        self.beaconId: int = 0
        self.model: str = ""
        self.adc: str = ""
        self.frequency: int = 0
        self.num_samples: int = 0
        self.sample_time: float = 0.0
        self.v_ref: int = 0
        self.port: int = 0
        self.uid: int = 0

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(87)
        buffer[0:1] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.resolution
        buffer[3] = self.channels
        buffer[4] = self.beaconId
        buffer[5:34] = self.model.encode(encoding_utf8)
        buffer[35:64] = self.adc.encode(encoding_utf8)
        buffer[65:68] = self.frequency.to_bytes(4, little_endian)
        buffer[69:72] = self.num_samples.to_bytes(4, little_endian)
        f = bytearray(struct.pack("f", self.sample_time))
        f.reverse()
        buffer[73:76] = f
        buffer[77:80] = self.v_ref.to_bytes(4, little_endian)
        buffer[81:84] = self.port.to_bytes(4, little_endian)
        buffer[85:86] = self.uid.to_bytes(2, little_endian)
        return buffer

    def from_bytearray(self, buffer: bytearray) -> bool:
        if len(buffer) != 85:
            return False
        if buffer[0:1] != magic_number.to_bytes(2, little_endian):
            return False
        self.resolution = buffer[2]
        self.channels = buffer[3]
        self.beaconId = buffer[4]
        self.model = buffer[5:34].decode(encoding_utf8, ignore_errors)
        self.adc = buffer[35:64].decode(encoding_utf8, ignore_errors)
        self.frequency = int.from_bytes(buffer[65:68], little_endian)
        self.num_samples = int.from_bytes(buffer[69:72], little_endian)
        b = buffer[73:76]
        b.reverse()
        self.sample_time = struct.unpack("f", b)
        self.v_ref = int.from_bytes(buffer[77:80], little_endian)
        self.port = int.from_bytes(buffer[81:84], little_endian)
        self.uid = int.from_bytes(buffer[85:86], little_endian)
        return True


class CommandHeader:

    def __init__(self):
        self.port: int = 0
        self.num_settings: int = 0
        self.trigger_setting_headers: List[TriggerSettingHeader] = []

    def to_bytearray(self) -> bytearray:
        self.num_settings = len(self.trigger_setting_headers)
        buffer = bytearray(8 + 6 * self.num_settings)
        buffer[0:1] = magic_number.to_bytes(2, little_endian)
        buffer[2:5] = self.port.to_bytes(4, little_endian)
        buffer[6:7] = self.num_settings.to_bytes(2, little_endian)
        for i in range(self.num_settings):
            offset = 6 * i
            buffer[8+offset:13+offset] = self.trigger_setting_headers[i].to_bytearray()
        return buffer

    def from_bytearray(self, buffer: bytearray) -> bool:
        if len(buffer) < 14:
            return False
        if buffer[0:1] != magic_number.to_bytes(2, little_endian):
            return False
        self.port = int.from_bytes(buffer[2:5], little_endian)
        self.num_settings = int.from_bytes(buffer[6:7], little_endian)
        if len(buffer) != 8 + 6 * self.num_settings:
            return False
        self.trigger_setting_headers = [None] * self.num_settings
        for i in range(self.num_settings):
            self.trigger_setting_headers[i] = TriggerSettingHeader()
            offset = 6 * i
            if self.trigger_setting_headers[i].from_bytearray(buffer[8+offset:13+offset]) is False:
                return False
        return True


class TriggerSettingHeader:

    def __init__(self):
        self.channel: int = 0
        self.trigger_voltage: int = 0
        self.active: bool = False

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(6)
        buffer[0] = self.channel
        buffer[1:4] = self.trigger_voltage.to_bytes(4, little_endian)
        buffer[5] = self.active
        return buffer

    def from_bytearray(self, buffer: bytearray) -> bool:
        self.channel = buffer[0]
        self.trigger_voltage = int.from_bytes(buffer[1:4], little_endian)
        self.active = bool(buffer[5])
        return True


class SampleTransmissionHeader:

    def __init__(self):
        self.frame_id: int = 0
        self.num_frames: int = 0
        self.transmission_group_id: int = 0
        self.resolution: int = 0
        self.channels: int = 0
        self.frequency: int = 0
        self.v_ref: int = 0
        self.num_samples: int = 0
        self.payload: bytearray = bytearray(0)

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(19 + len(self.payload))
        buffer[0:1] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.frame_id
        buffer[3] = self.num_frames
        buffer[4] = self.transmission_group_id
        buffer[5] = self.resolution
        buffer[6] = self.channels
        buffer[7:10] = self.frequency.to_bytes(4, little_endian)
        buffer[11:14] = self.v_ref.to_bytes(4, little_endian)
        buffer[15:18] = self.num_samples.to_bytes(4, little_endian)
        buffer[19:] = self.payload
        return buffer

    def from_bytearray(self, buffer: bytearray) -> bool:
        if len(buffer) < 19:
            return False
        if buffer[0:1] != magic_number.to_bytes(2, little_endian):
            return False
        self.frame_id = buffer[2]
        self.num_frames = buffer[3]
        if self.frame_id >= self.num_frames:
            return False
        self.transmission_group_id = buffer[4]
        self.resolution = buffer[5]
        self.channels = buffer[6]
        self.frequency = int.from_bytes(buffer[7:10], little_endian)
        self.v_ref = int.from_bytes(buffer[11:14], little_endian)
        self.num_samples = int.from_bytes(buffer[15:18], little_endian)
        if len(buffer) != 19 + self.num_samples * get_bytes_per_sample(self.resolution):
            return False
        self.payload = buffer[19:]
        return True

    def same_transmission_group(self, other):
        if self.num_frames != other.num_frames:
            return False
        if self.transmission_group_id != other.transmission_group_id:
            return False
        if self.resolution != other.resolution:
            return False
        if self.channels != other.channels:
            return False
        if self.frequency != other.frequency:
            return False
        if self.v_ref != other.v_ref:
            return False
        return True

