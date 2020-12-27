# Enable recursive typing for python 3.7+ (from 3.10 it is build-in)
from __future__ import annotations

from osziplotter.modelcontroller.BoardInfo import BoardInfo
from osziplotter.modelcontroller.PlotEvents import PlotEvents

from typing import Dict, Type, List


class BoardEvents:

    __board_list: Dict[int, BoardInfo] = {}
    __listeners: List[Type[BoardEvents]] = []
    __selected_board: int = -1

    def __init__(self):
        self.__listenerId = len(BoardEvents.__listeners)
        BoardEvents.__listeners.append(self)

    @classmethod
    def put(cls, info: BoardInfo) -> None:
        if info.uid not in BoardEvents.__board_list:
            BoardEvents.__board_list[info.uid] = info
            BoardEvents.__update_listeners()
        elif BoardEvents.__board_list[info.uid] != info:
            BoardEvents.__board_list[info.uid] = info
            BoardEvents.__update_listeners()

    # call this every second once to handle timeouts
    @classmethod
    def tick(cls) -> None:
        for board in BoardEvents.__board_list.values():
            if board.is_timeout(timeout=3.5):
                BoardEvents.__board_list.pop(board.uid)
                BoardEvents.__update_listeners()

    @classmethod
    def __update_listeners(cls) -> None:
        for listener in BoardEvents.__listeners:
            listener.update_boards(BoardEvents.__board_list, BoardEvents.__selected_board)

    @classmethod
    def update_selected_board(cls, selected_board: int) -> None:
        BoardEvents.__selected_board = selected_board
        PlotEvents.__update_selected_board(selected_board)

    # Overwrite this method if you want to react on it
    def update_boards(self, board_list: List[BoardInfo], selected_board: int) -> None:
        pass
