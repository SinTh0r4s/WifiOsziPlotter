from socket import socket, AF_INET, SOCK_DGRAM, error
from errno import EAGAIN, EWOULDBLOCK
from SampleCollector import SampleCollector
from BoardCollector import BoardCollector
from typing import Callable
from Headers import BeaconHeader, SampleTransmissionHeader, CommandHeader, TriggerSettingHeader


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
            buffer = self.socket.recv(4096)
            if len(buffer) > 0:
                beacon = BeaconHeader()
                if beacon.from_bytearray(buffer):
                    self.board_collector.on_board_received(beacon)
                samples = SampleTransmissionHeader()
                if samples.from_bytearray(buffer):
                    self.sample_collector.process_received_sample_transmission_header(samples)
        except error as e:
            err = e.args[0]
            if err != EAGAIN and err != EWOULDBLOCK:
                print("Fatal socket error!")

        self.board_collector.handle_events()


if __name__ == "__main__":
    def draw():
        print("draw")

    def update_boards():
        print("update boards")

    network = Network(draw, update_boards)
    while True:
        network.handle_events()
