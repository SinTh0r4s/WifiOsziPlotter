from osziplotter.modelcontroller.PlotEvents import PlotEvents
from osziplotter.modelcontroller.PlotInfo import PlotInfo

from PyQt5.QtWidgets import QPushButton, QFileDialog
from typing import Dict
from scipy.io import savemat


class ExportWidget(QPushButton, PlotEvents):

    def __init__(self, *args, **kwargs) -> None:
        super(ExportWidget, self).__init__("Export to Matlab", *args, **kwargs)
        self.clicked.connect(self._export)
        self.setDisabled(True)
        self._current_plot: PlotInfo = None

    def _export(self) -> None:
        filename, _ = QFileDialog().getSaveFileName(self, "Save plot as ...", filter="Matlab Data File (*.mat)")
        if filename != "":
            savemat(filename, self._current_plot.to_dict())

    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        self._current_plot = visible_plot
        self.setDisabled(visible_plot is None)
