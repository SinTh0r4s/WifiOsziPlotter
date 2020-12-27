from osziplotter.Util import to_one_decimal
from osziplotter.modelcontroller.BoardEvents import BoardEvents
from osziplotter.modelcontroller.BoardInfo import BoardInfo

from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout
from typing import List, Dict


class BoardInfoLabel(QWidget, BoardEvents):
    
    def __init__(self, *args, **kwargs):
        super(BoardInfoLabel, self).__init__(*args, **kwargs)
        self._row_counter = 0
        self._name_labels: List[QLabel] = []

        self._layout = QGridLayout(self)

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
        self._layout.addWidget(label, self._row_counter, 1)
        self._name_labels.append(label)
        label = QLabel("")
        self._layout.addWidget(label, self._row_counter, 2)
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
            sample_time = board.num_samples / board.frequency
            sample_time_unit = "s"
            if sample_time < 1.0:
                sample_time = sample_time * 1000
                sample_time_unit = "ms"
            if sample_time < 1.0:
                sample_time = sample_time * 1000
                sample_time_unit = "ys"
            if sample_time < 1.0:
                sample_time = sample_time * 1000
                sample_time_unit = "ns"
            self._sample_time_label.setText(to_one_decimal(sample_time) + sample_time_unit)
            self._num_samples_label.setText(str(board.num_samples))
            self._num_channels_label.setText(str(board.num_channels))
            frequency = board.frequency
            frequency_unit = "Hz"
            if frequency > 1000:
                frequency = frequency / 1000
                frequency_unit = "kHz"
            if frequency > 1000:
                frequency = frequency / 1000
                frequency_unit = "MHz"
            if frequency > 1000:
                frequency = frequency / 1000
                frequency_unit = "GHz"
            self._frequency_label.setText(to_one_decimal(frequency) + frequency_unit)
            self._v_ref_label.setText(str(board.v_ref) + "mV")
            self._resolution_label.setText(str(board.resolution) + "bits")
