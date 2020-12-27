# Enable recursive typing for python 3.7+ (from 3.10 it is build-in)
from __future__ import annotations

from osziplotter.modelcontroller.BoardInfo import BoardInfo
from osziplotter.modelcontroller.PlotEvents import PlotEvents

from typing import Dict, Type, List


class BoardEvents:

    _board_list: Dict[int, BoardInfo] = {}
    _listeners: List[Type[BoardEvents]] = []
    _selected_board: int = -1

    def __init__(self):
        self._listenerId = len(BoardEvents._listeners)
        BoardEvents._listeners.append(self)

    @classmethod
    def put(cls, info: BoardInfo) -> None:
        if info.uid not in BoardEvents._board_list:
            BoardEvents._board_list[info.uid] = info
            BoardEvents._update_listeners()
        elif BoardEvents._board_list[info.uid] != info:
            BoardEvents._board_list[info.uid] = info
            BoardEvents._update_listeners()

    # call this every second once to handle timeouts
    @classmethod
    def tick(cls) -> None:
        for board in BoardEvents._board_list.values():
            if board.is_timeout(timeout=3.5):
                BoardEvents._board_list.pop(board.uid)
                BoardEvents._update_listeners()

    @classmethod
    def _update_listeners(cls) -> None:
        for listener in BoardEvents._listeners:
            listener.update_boards(BoardEvents._board_list, BoardEvents._selected_board)

    @classmethod
    def update_selected_board(cls, selected_board: int) -> None:
        BoardEvents._selected_board = selected_board
        PlotEvents._update_selected_board(selected_board)

    # Overwrite this method if you want to react on it
    def update_boards(self, board_list: List[BoardInfo], selected_board: int) -> None:
        pass
