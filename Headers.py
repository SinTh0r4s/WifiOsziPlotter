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
        self.num_settings: int = 0
        self.address: str = ""
        self.trigger_setting_headers: List[TriggerSettingHeader] = []

    def to_bytearray(self) -> bytearray:
        self.num_settings = len(self.trigger_setting_headers)
        buffer = bytearray(7 + 6 * self.num_settings)
        buffer[0:2] = magic_number.to_bytes(2, little_endian)
        buffer[2:6] = self.port.to_bytes(4, little_endian)
        buffer[6] = self.num_settings
        for i in range(self.num_settings):
            offset = 6 * i
            buffer[7+offset:13+offset] = self.trigger_setting_headers[i].to_bytearray()
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        if len(buffer) < 13:
            return False
        if magic_number != int.from_bytes(buffer[0:2], little_endian):
            return False
        self.port = int.from_bytes(buffer[2:6], little_endian)
        self.num_settings = buffer[6]
        if len(buffer) != 7 + 6 * self.num_settings:
            return False
        self.trigger_setting_headers = [None] * self.num_settings
        for i in range(self.num_settings):
            self.trigger_setting_headers[i] = TriggerSettingHeader()
            offset = 6 * i
            if self.trigger_setting_headers[i].from_bytearray(buffer[7+offset:13+offset]) is False:
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
        buffer[1:5] = self.trigger_voltage.to_bytes(4, little_endian)
        buffer[5] = self.active
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        self.channel = buffer[0]
        self.trigger_voltage = int.from_bytes(buffer[1:5], little_endian)
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


# Tests
if __name__ == "__main__":
    beacon = BeaconHeader()
    beacon.beaconId = 11
    beacon.v_ref = 3300
    beacon.port = 12345
    beacon.num_samples = 10000
    beacon.sample_time = 0.1
    beacon.frequency = 100000
    beacon.resolution = 8
    beacon.model = "Leona OTP FTW"
    beacon.channels = 1
    beacon.uid = 5433
    beacon.adc = "Just kidding"
    beacon_bin = beacon.to_bytearray()
    beacon_copy = BeaconHeader()
    beacon_copy.from_bytearray(beacon_bin)
    print("Original beacon: " + str(beacon.__dict__))
    print("Bin copy beacon: " + str(beacon_copy.__dict__))

    command = CommandHeader()
    command.port = 1234
    command.num_settings = 2
    command.trigger_setting_headers = [TriggerSettingHeader(), TriggerSettingHeader()]
    command.trigger_setting_headers[0].trigger_voltage = 200
    command.trigger_setting_headers[0].active = True
    command.trigger_setting_headers[0].channel = 1
    command.trigger_setting_headers[0].trigger_voltage = 3000
    command.trigger_setting_headers[0].active = False
    command.trigger_setting_headers[0].channel = 4
    command_bin = command.to_bytearray()
    command_copy = CommandHeader()
    command_copy.from_bytearray(command_bin)
    print("Original command: " + str(command.__dict__))
    print("Bin copy command: " + str(command_copy.__dict__))
    for i in range(len(command.trigger_setting_headers)):
        print("    Original trigger: " + str(command.trigger_setting_headers[i].__dict__))
        print("    Bin copy trigger: " + str(command_copy.trigger_setting_headers[i].__dict__))

    samples = SampleTransmissionHeader()
    samples.num_samples = 1
    samples.v_ref = 3300
    samples.channels = 1
    samples.resolution = 8
    samples.frequency = 100000
    samples.transmission_group_id = 123
    samples.num_frames = 1
    samples.frame_id = 0
    samples.payload = bytearray(1)
    samples_bin = samples.to_bytearray()
    samples_copy = SampleTransmissionHeader()
    samples_copy.from_bytearray(samples_bin)
    print("Original samples: " + str(samples.__dict__))
    print("Bin copy samples: " + str(samples_copy.__dict__))
