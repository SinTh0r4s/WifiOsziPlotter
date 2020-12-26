from BoardInfo import BoardInfo
from Headers import BeaconHeader
from typing import Callable


class BoardCollector:

    def __init__(self, refresh_boards_callback: Callable):
        self.boards: dict[int, BoardInfo] = {}
        self.refresh_boards_callback: Callable = refresh_boards_callback

    def on_board_received(self, beacon: BeaconHeader):
        info = BoardInfo(beacon)
        if info.uid not in self.boards:
            self.boards[info.uid] = info
            self.refresh_boards_callback()
        self.boards[info.uid] = info

    def handle_events(self):
        for uid in self.boards:
            if self.boards[uid].is_timeout():
                self.boards.pop(uid)
                self.refresh_boards_callback()
