from osziplotter.modelcontroller.PlotEvents import PlotEvents
from osziplotter.modelcontroller.PlotInfo import PlotInfo

from PyQt5.QtWidgets import QPushButton
from typing import Dict, List


class ExportWidget(QPushButton, PlotEvents):

    def __init__(self, *args, **kwargs):
        super(ExportWidget, self).__init__("Export", *args, **kwargs)
        self.clicked.connect(self._export)

    def _export(self):
        pass

    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        pass
