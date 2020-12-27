from typing import List
from Util import get_bytes_per_sample
from struct import unpack, pack

magic_number: int = 0x7567
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
        self.address: str = ""

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(87)
        buffer[0:2] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.resolution
        buffer[3] = self.channels
        buffer[4] = self.beaconId
        buffer[5:5+len(self.model)] = self.model.encode(encoding_utf8)
        buffer[35:35+len(self.adc)] = self.adc.encode(encoding_utf8)
        buffer[65:69] = self.frequency.to_bytes(4, little_endian)
        buffer[69:73] = self.num_samples.to_bytes(4, little_endian)
        f = bytearray(pack("f", self.sample_time))
        f.reverse()
        buffer[73:77] = f
        buffer[77:81] = self.v_ref.to_bytes(4, little_endian)
        buffer[81:85] = self.port.to_bytes(4, little_endian)
        buffer[85:87] = self.uid.to_bytes(2, little_endian)
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        if len(buffer) != 87:
            return False
        if magic_number != int.from_bytes(buffer[0:2], little_endian):
            return False
        self.resolution = buffer[2]
        self.channels = buffer[3]
        self.beaconId = buffer[4]
        self.model = buffer[5:35].decode(encoding_utf8, ignore_errors).rstrip('\x00')
        self.adc = buffer[35:65].decode(encoding_utf8, ignore_errors).rstrip('\x00')
        self.frequency = int.from_bytes(buffer[65:69], little_endian)
        self.num_samples = int.from_bytes(buffer[69:73], little_endian)
        b = bytearray(buffer[73:77])
        b.reverse()
        self.sample_time, = unpack("f", b)
        self.v_ref = int.from_bytes(buffer[77:81], little_endian)
        self.port = int.from_bytes(buffer[81:85], little_endian)
        self.uid = int.from_bytes(buffer[85:87], little_endian)
        return True


class CommandHeader:

    def __init__(self):
        self.port: int = 0
        self.channel: int = 0
        self.trigger_voltage: int = 0
        self.active: bool = False
        self.address: str = ""

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(12)
        buffer[0:2] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.channel
        buffer[3] = self.active
        buffer[4:8] = self.trigger_voltage.to_bytes(4, little_endian)
        buffer[8:12] = self.port.to_bytes(4, little_endian)
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        if len(buffer) != 12:
            return False
        if magic_number != int.from_bytes(buffer[0:2], little_endian):
            return False
        self.channel = buffer[2]
        self.active = buffer[3]
        self.trigger_voltage = int.from_bytes(buffer[4:8], little_endian)
        self.port = int.from_bytes(buffer[8:12], little_endian)
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
        self.address: str = ""
        self.payload: bytearray = bytearray(0)

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(19 + len(self.payload))
        buffer[0:2] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.frame_id
        buffer[3] = self.num_frames
        buffer[4] = self.transmission_group_id
        buffer[5] = self.resolution
        buffer[6] = self.channels
        buffer[7:11] = self.frequency.to_bytes(4, little_endian)
        buffer[11:15] = self.v_ref.to_bytes(4, little_endian)
        buffer[15:19] = self.num_samples.to_bytes(4, little_endian)
        buffer[19:] = self.payload
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        if len(buffer) < 19:
            return False
        if magic_number != int.from_bytes(buffer[0:2], little_endian):
            return False
        self.frame_id = buffer[2]
        self.num_frames = buffer[3]
        if self.frame_id >= self.num_frames:
            return False
        self.transmission_group_id = buffer[4]
        self.resolution = buffer[5]
        self.channels = buffer[6]
        self.frequency = int.from_bytes(buffer[7:11], little_endian)
        self.v_ref = int.from_bytes(buffer[11:15], little_endian)
        self.num_samples = int.from_bytes(buffer[15:19], little_endian)
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
