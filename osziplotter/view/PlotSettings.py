from osziplotter.modelcontroller.PlotEvents import PlotEvents
from osziplotter.modelcontroller.PlotInfo import PlotInfo
from osziplotter.modelcontroller.Enums import Domain

from PyQt5.QtWidgets import QPushButton
from typing import Dict


class PlotSettings(QPushButton, PlotEvents):

    def __init__(self, *args, **kwargs) -> None:
        super(PlotSettings, self).__init__(Domain.time, *args, **kwargs)
        self.clicked.connect(self._toggle)
        self.setDisabled(True)

    def _toggle(self) -> None:
        if self.text() == Domain.time:
            self.setText(Domain.frequency)
            self.update_plot_domain(Domain.frequency)
        else:
            self.setText(Domain.time)
            self.update_plot_domain(Domain.time)

    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        self.setDisabled(visible_plot is None)
        self.setText(visible_plot.domain)
