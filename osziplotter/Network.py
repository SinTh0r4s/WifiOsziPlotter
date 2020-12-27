from socket import socket, AF_INET, SOCK_DGRAM, error
from errno import EAGAIN, EWOULDBLOCK
from SampleCollector import SampleCollector
from BoardCollector import BoardCollector
from BoardInfo import BoardInfo
from typing import Callable, List
from Headers import BeaconHeader, SampleTransmissionHeader, CommandHeader


class Network:

    def __init__(self, draw_callback: Callable, update_boards_callback: Callable):
        self.updateBoardsCallback = None
        self.sample_collector = SampleCollector(draw_callback)
        self.board_collector = BoardCollector(update_boards_callback)

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", 7567))
        self.socket.setblocking(False)

    def handle_events(self):
        try:
            buffer, address = self.socket.recvfrom(4096)
            if len(buffer) > 0:
                beacon = BeaconHeader()
                if beacon.from_bytearray(buffer):
                    beacon.address = address[0]
                    self.board_collector.on_board_received(beacon)
                    return
                samples = SampleTransmissionHeader()
                if samples.from_bytearray(buffer):
                    samples.address = address[0]
                    self.sample_collector.process_received_sample_transmission_header(samples)
        except error as e:
            err = e.args[0]
            if err != EAGAIN and err != EWOULDBLOCK:
                print("Fatal socket error!")

        self.board_collector.handle_events()

    def send_trigger(self, target: BoardInfo, channel: int, active: bool, trigger_voltage: int):
        command = CommandHeader()
        command.port = 7567
        command.active = active
        command.trigger_voltage = trigger_voltage
        command.channel = channel
        command_bin = command.to_bytearray()
        self.socket.sendto(command_bin, (target.ip, command.port))

    def get_boards(self) -> List[BoardInfo]:
        return self.board_collector.get_boards()


if __name__ == "__main__":
    def draw(data):
        print("draw")
        print(data)
        print(len(data[0]))

    def update_boards():
        print("update boards")

    network = Network(draw, update_boards)
    import time
    t = time.time()
    once = False
    while True:
        network.handle_events()
        if time.time() - t > 3 and not once:
            print("Sending trigger settings")
            boards = network.get_boards()
            network.send_trigger(boards[0], 1, True, 647)
            t = time.time()
            once = True
