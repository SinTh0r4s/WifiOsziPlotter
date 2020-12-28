from osziplotter.Util import to_one_decimal, get_frequency_readable, get_timesteps_readable
from osziplotter.modelcontroller.BoardEvents import BoardEvents
from osziplotter.modelcontroller.BoardInfo import BoardInfo

from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout
from typing import List, Dict


class BoardInfoLabel(QWidget, BoardEvents):
    
    def __init__(self, *args, **kwargs):
        super(BoardInfoLabel, self).__init__(*args, **kwargs)
        self._row_counter = 0
        self._name_labels: List[QLabel] = []

        self.setLayout(QGridLayout())

        self._uid_label = self._add_label("Unique ID")
        self._model_label = self._add_label("Model")
        self._adc_label = self._add_label("ADC")
        self._sample_time_label = self._add_label("Sample time")
        self._num_samples_label = self._add_label("# Samples")
        self._num_channels_label = self._add_label("# Channels")
        self._frequency_label = self._add_label("Frequency")
        self._v_ref_label = self._add_label("Vref")
        self._resolution_label = self._add_label("Resolution")

    def _add_label(self, name: str) -> QLabel:
        label = QLabel(name)
        self.layout().addWidget(label, self._row_counter, 1)
        self._name_labels.append(label)
        label = QLabel("")
        self.layout().addWidget(label, self._row_counter, 2)
        self._row_counter += 1
        return label

    def update_boards(self, board_list: Dict[int, BoardInfo], selected_board: int) -> None:
        if selected_board == -1:
            self._uid_label.setText("")
            self._model_label.setText("")
            self._adc_label.setText("")
            self._sample_time_label.setText("")
            self._num_samples_label.setText("")
            self._num_channels_label.setText("")
            self._frequency_label.setText("")
            self._v_ref_label.setText("")
            self._resolution_label.setText("")
        else:
            board = board_list[selected_board]
            self._uid_label.setText(hex(board.uid))
            self._model_label.setText(board.model)
            self._adc_label.setText(board.adc)
            sample_time, sample_time_unit = get_timesteps_readable(board.num_samples / board.frequency)
            self._sample_time_label.setText(to_one_decimal(sample_time) + sample_time_unit)
            self._num_samples_label.setText(str(board.num_samples))
            self._num_channels_label.setText(str(board.num_channels))
            (frequency, frequency_unit) = get_frequency_readable(board.frequency)
            self._frequency_label.setText(to_one_decimal(frequency) + frequency_unit)
            self._v_ref_label.setText(str(board.v_ref) + "mV")
            self._resolution_label.setText(str(board.resolution) + "bits")
