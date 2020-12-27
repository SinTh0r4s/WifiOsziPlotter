from osziplotter.modelcontroller.BoardEvents import BoardEvents
from osziplotter.modelcontroller.BoardInfo import BoardInfo
from osziplotter.network.Network import Network

from PyQt5.QtWidgets import QLabel, QWidget, QSpinBox, QPushButton, QHBoxLayout, QComboBox, QVBoxLayout
from typing import Dict


class TriggerCommandWidget(QWidget, BoardEvents):

    def __init__(self, network: Network, *args, **kwargs):
        super(TriggerCommandWidget, self).__init__(*args, **kwargs)
        self._target_ip: str = ""
        self._target_port: int = 0
        self._network: Network = network
        self._selected_channel: int = 1

        self.setLayout(QVBoxLayout())

        self._channel_layout = QHBoxLayout()
        self._channel_label = QLabel("Channel")
        self._channel_layout.addWidget(self._channel_label)
        self._channel_combobox = QComboBox()
        self._channel_combobox.activated.connect(self._select_channel)
        self._channel_combobox.setDisabled(True)
        self._channel_layout.addWidget(self._channel_combobox)
        self.layout().addLayout(self._channel_layout)

        self._voltage_layout = QHBoxLayout()
        self._voltage_description_label = QLabel("Trigger voltage")
        self._voltage_layout.addWidget(self._voltage_description_label)
        self._input = QSpinBox()
        self._input.setMinimum(0)
        self._input.setMaximum(9999)
        self._input.setDisabled(True)
        self._voltage_layout.addWidget(self._input)
        self._unit_label = QLabel("mV")
        self._voltage_layout.addWidget(self._unit_label)
        self.layout().addLayout(self._voltage_layout)

        self._button_layout = QHBoxLayout()
        self._set_button = QPushButton("Set")
        self._set_button.clicked.connect(self._set_trigger)
        self._set_button.setDisabled(True)
        self._button_layout.addWidget(self._set_button)
        self._disarm_button = QPushButton("Disarm")
        self._disarm_button.clicked.connect(self._disarm_trigger)
        self._disarm_button.setDisabled(True)
        self._button_layout.addWidget(self._disarm_button)
        self.layout().addLayout(self._button_layout)

    def _set_trigger(self):
        self._network.send_trigger((self._target_ip, self._target_port), 1, True, self._input.value())
        self._disarm_button.setEnabled(True)

    def _disarm_trigger(self):
        self._network.send_trigger((self._target_ip, self._target_port), 1, False, self._input.value())
        self._disarm_button.setDisabled(True)

    def _select_channel(self, index: int):
        self._selected_channel = index + 1
        print(str(index+1))

    def update_boards(self, board_list: Dict[int, BoardInfo], selected_board: int) -> None:
        if selected_board == -1:
            self._input.setDisabled(True)
            self._set_button.setDisabled(True)
            self._disarm_button.setDisabled(True)
            self._channel_combobox.setDisabled(True)
        else:
            self._input.setEnabled(True)
            self._set_button.setEnabled(True)
            board = board_list[selected_board]
            self._input.setMaximum(board.v_ref)
            self._target_ip = board.ip
            self._target_port = board.port
            self._channel_combobox.setEnabled(board.num_channels > 1)
            self._channel_combobox.clear()
            for channel in range(board.num_channels):
                self._channel_combobox.addItem(str(channel+1))
            if self._selected_channel <= board.num_channels:
                self._channel_combobox.setCurrentIndex(self._selected_channel-1)
            else:
                self._channel_combobox.setCurrentIndex(0)
                self._selected_channel = 1
