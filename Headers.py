import struct

magic_number: int = 7567


class BeaconHeader:

    def __init__(self):
        self.resolution: int = 0
        self.channels: int = 0
        self.model: str = ""
        self.adc: str = ""
        self.frequency: int = 0
        self.num_samples: int = 0
        self.sample_time: float = 0.0
        self.v_ref: int = 0
        self.port: int = 0

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(84)
        buffer[0:1] = magic_number.to_bytes(2, 'little')
        buffer[2] = self.resolution
        buffer[3] = self.channels
        buffer[4:33] = self.model.encode('utf-8')
        buffer[34:63] = self.adc.encode('utf-8')
        buffer[64:67] = self.frequency.to_bytes(4, 'little')
        buffer[68:71] = self.num_samples.to_bytes(4, 'little')
        f = bytearray(struct.pack("f", self.sample_time))
        f.reverse()
        buffer[72:75] = f
        buffer[76:79] = self.v_ref.to_bytes(4, 'little')
        buffer[80:83] = self.port.to_bytes(4, 'little')
        return buffer


class CommandHeader:

    def __init__(self):
        self.port: int = 0
        self.num_settings: int = 0
        self.trigger_setting_headers: [TriggerSettingHeader]

    def to_bytearray(self) -> bytearray:
        self.num_settings = len(self.trigger_settings_headers)
        buffer = bytearray(7 + 6 * self.num_settings)
        buffer[0:1] = magic_number.to_bytes(2, 'little')
        buffer[2:5] = self.port.to_bytes(4, 'little')
        buffer[6:7] = self.num_settings.to_bytes(2, 'little')
        for i in range(self.num_settings):
            offset = 6 * i
            buffer[8+offset:13+offset] = self.trigger_setting_headers[i].to_bytearray()
        return buffer


class TriggerSettingHeader:

    def __init__(self):
        self.channel: int = 0
        self.trigger_voltage: int = 0
        self.active: bool = False

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(6)
        buffer[0] = self.channel
        buffer[1:4] = self.trigger_voltage.to_bytes(4, 'little')
        buffer[5] = self.active
        return buffer


class SampleTransmissionHeader:

    def __init__(self):
        self.frame_id: int = 0
        self.num_frames: int = 0
        self.resolution: int = 0
        self.channels: int = 0
        self.frequency: int = 0
        self.v_ref: int = 0
        self.num_samples: int = 0

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(18);
        buffer[0:1] = magic_number.to_bytes(2, 'little')
        buffer[2] = self.frame_id
        buffer[3] = self.num_frames
        buffer[4] = self.resolution
        buffer[5] = self.channels
        buffer[6:9] = self.frequency.to_bytes(4, 'little')
        buffer[10:13] = self.v_ref.to_bytes(4, 'little')
        buffer[14:17] = self.num_samples.to_bytes(4, 'little')
        return buffer
