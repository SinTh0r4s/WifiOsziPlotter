from osziplotter.network.Headers import BeaconHeader, SampleTransmissionHeader, CommandHeader
from osziplotter.network.SampleCollector import SampleCollector
from osziplotter.modelcontroller.BoardInfo import BoardInfo
from osziplotter.modelcontroller.BoardEvents import BoardEvents

from socket import socket, AF_INET, SOCK_DGRAM, error
from errno import EAGAIN, EWOULDBLOCK


class Network(BoardEvents):

    def __init__(self):
        super(Network, self).__init__()
        self.sample_collector = SampleCollector()
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def listen(self) -> None:
        self.socket.bind(("", 7567))
        self.socket.setblocking(False)

    def handle_events(self) -> None:
        try:
            buffer, address = self.socket.recvfrom(4096)
            if len(buffer) > 0:
                beacon = BeaconHeader()
                if beacon.from_bytearray(buffer):
                    beacon.address = address[0]
                    self.put(beacon.to_board_info())
                    return
                samples = SampleTransmissionHeader()
                if samples.from_bytearray(buffer):
                    samples.address = address[0]
                    self.sample_collector.process_received_sample_transmission_header(samples)
        except error as e:
            err = e.args[0]
            if err != EAGAIN and err != EWOULDBLOCK:
                print("Fatal socket error!")

    def send_trigger(self, target: BoardInfo, channel: int, active: bool, trigger_voltage: int) -> None:
        command = CommandHeader()
        command.port = 7567
        command.active = active
        command.trigger_voltage = trigger_voltage
        command.channel = channel
        command_bin = command.to_bytearray()
        self.socket.sendto(command_bin, (target.ip, command.port))
