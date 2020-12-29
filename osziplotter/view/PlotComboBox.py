from osziplotter.Util import get_timestamp_readable
from osziplotter.modelcontroller.PlotEvents import PlotEvents
from osziplotter.modelcontroller.PlotInfo import PlotInfo

from PyQt5.QtWidgets import QComboBox
from typing import Dict, List


class PlotComboBox(QComboBox, PlotEvents):

    def __init__(self, *args, **kwargs):
        super(PlotComboBox, self).__init__(*args, **kwargs)
        self.setDisabled(True)
        self.addItem("No plot available")
        self.activated.connect(self._select_plot)
        self._timestamps: List[float] = []

    def _select_plot(self, index: int) -> None:
        self.update_selected_plot(self._timestamps[index])

    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        self.clear()
        if visible_plot is None:
            self.setDisabled(True)
            self.addItem("No plot available")
        else:
            self.setEnabled(True)
            timestamps_str = [get_timestamp_readable(plot.timestamp) for plot in plots.values()]
            self.addItems(timestamps_str)
            self._timestamps = [plot.timestamp for plot in plots.values()]
            self.setCurrentIndex(list(plots.values()).index(visible_plot))

