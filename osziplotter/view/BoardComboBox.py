from osziplotter.modelcontroller.BoardEvents import BoardEvents
from osziplotter.modelcontroller.BoardInfo import BoardInfo

from PyQt5.QtWidgets import QComboBox
from typing import Dict, List


class BoardComboBox(QComboBox, BoardEvents):

    def __init__(self, *args, **kwargs):
        super(BoardComboBox, self).__init__(*args, **kwargs)
        self.setDisabled(True)
        self.addItem("No board available")
        self.activated.connect(self._select_board)
        self._uids: List[int] = []

    def _select_board(self, index: int):
        self.update_selected_board(self._uids[index])

    def update_boards(self, board_list: Dict[int, BoardInfo], selected_board: int) -> None:
        self.clear()
        if selected_board == -1:
            self.setDisabled(True)
            self.addItem("No board available")
        else:
            self.setEnabled(True)
            self.addItems([str(board) for board in board_list.values()])
            self._uids = [board.uid for board in board_list.values()]
            self.setCurrentIndex(self._uids.index(selected_board))

