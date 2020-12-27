from osziplotter.Util import get_bytes_per_sample
from osziplotter.modelcontroller.BoardInfo import BoardInfo
from osziplotter.modelcontroller.PlotInfo import PlotInfo

from struct import unpack, pack

magic_number: int = 0x7567
little_endian: str = "little"
encoding_utf8: str = "utf-8"
ignore_errors: str = "ignore"


class BeaconHeader:

    def __init__(self):
        self.resolution: int = 0
        self.num_channels: int = 0
        self.beaconId: int = 0
        self.model: str = ""
        self.adc: str = ""
        self.frequency: int = 0
        self.num_samples: int = 0
        self.v_ref: int = 0
        self.port: int = 0
        self.uid: int = 0

        self.address: str = ""

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(83)
        buffer[0:2] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.resolution
        buffer[3] = self.num_channels
        buffer[4] = self.beaconId
        buffer[5:5+len(self.model)] = self.model.encode(encoding_utf8)
        buffer[35:35+len(self.adc)] = self.adc.encode(encoding_utf8)
        buffer[65:69] = self.frequency.to_bytes(4, little_endian)
        buffer[69:73] = self.num_samples.to_bytes(4, little_endian)
        buffer[73:77] = self.v_ref.to_bytes(4, little_endian)
        buffer[77:81] = self.port.to_bytes(4, little_endian)
        buffer[81:83] = self.uid.to_bytes(2, little_endian)
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        if len(buffer) != 83:
            return False
        if magic_number != int.from_bytes(buffer[0:2], little_endian):
            return False
        self.resolution = buffer[2]
        self.num_channels = buffer[3]
        self.beaconId = buffer[4]
        self.model = buffer[5:35].decode(encoding_utf8, ignore_errors).rstrip('\x00')
        self.adc = buffer[35:65].decode(encoding_utf8, ignore_errors).rstrip('\x00')
        self.frequency = int.from_bytes(buffer[65:69], little_endian)
        self.num_samples = int.from_bytes(buffer[69:73], little_endian)
        self.v_ref = int.from_bytes(buffer[73:77], little_endian)
        self.port = int.from_bytes(buffer[77:81], little_endian)
        self.uid = int.from_bytes(buffer[81:83], little_endian)
        return True

    def to_board_info(self) -> BoardInfo:
        board: BoardInfo = BoardInfo()
        board.model = self.model
        board.adc = self.adc
        board.resolution = self.resolution
        board.num_samples = self.num_samples
        board.num_channels = self.num_channels
        board.frequency = self.frequency
        board.v_ref = self.v_ref
        board.uid = self.uid
        board.ip = self.address
        return board


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
        self.uid: int = 0
        self.payload: bytearray = bytearray(0)

        self.address: str = ""

    def to_bytearray(self) -> bytearray:
        buffer = bytearray(21 + len(self.payload))
        buffer[0:2] = magic_number.to_bytes(2, little_endian)
        buffer[2] = self.frame_id
        buffer[3] = self.num_frames
        buffer[4] = self.transmission_group_id
        buffer[5] = self.resolution
        buffer[6] = self.channels
        buffer[7:11] = self.frequency.to_bytes(4, little_endian)
        buffer[11:15] = self.v_ref.to_bytes(4, little_endian)
        buffer[15:19] = self.num_samples.to_bytes(4, little_endian)
        buffer[19:21] = self.uid.to_bytes(2, little_endian)
        buffer[21:] = self.payload
        return buffer

    def from_bytearray(self, buffer: bytes) -> bool:
        if len(buffer) < 21:
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
        if len(buffer) != 21 + self.num_samples * get_bytes_per_sample(self.resolution):
            return False
        self.uid = int.from_bytes(buffer[19:21], little_endian)
        self.payload = buffer[21:]
        return True

    def same_transmission_group(self, other) -> bool:
        return self.num_frames == other.num_frames\
            and self.transmission_group_id == other.transmission_group_id\
            and self.resolution == other.resolution\
            and self.channels == other.num_channels\
            and self.frequency == other.frequency\
            and self.v_ref == other.v_ref\
            and self.uid == other.uid

    def to_plot_info(self) -> PlotInfo:
        plot = PlotInfo()
        plot.resolution = self.resolution
        plot.channels = self.channels
        plot.frequency = self.frequency
        plot.v_ref = self.v_ref
        plot.num_samples = self.num_samples
        plot.board_uid = self.uid
        return plot
