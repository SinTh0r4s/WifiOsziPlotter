from osziplotter.modelcontroller.PlotEvents import PlotEvents
from osziplotter.modelcontroller.PlotInfo import PlotInfo
from osziplotter.Util import get_timestamp_readable, get_timesteps_readable

from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from typing import Dict
import numpy as np


class PlotWidget(QWidget, PlotEvents):
    def __init__(self, *args, **kwargs) -> None:
        super(PlotWidget, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self._canvas = PlotCanvas(self, width=10, height=8)
        self._toolbar = NavigationToolbar2QT(self._canvas, self)
        self.layout().addWidget(self._toolbar)
        self.layout().addWidget(self._canvas)

    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        self._canvas.update_plot(visible_plot)


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width: int = 10, height: int = 8, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def update_plot(self, visible_plot: PlotInfo = None) -> None:
        self.figure.clf()
        if visible_plot is not None:
            ax = self.figure.add_subplot(111)
            ax.set_title("Samples taken at " + get_timestamp_readable(visible_plot.timestamp))
            sample_time_unit = "s"
            sample_time = 1
            for channel in visible_plot.channels:
                plot = visible_plot.channels[channel]
                num_samples = len(plot)
                sample_time, sample_time_unit = get_timesteps_readable(num_samples / visible_plot.frequency)
                timestamps = np.linspace(0, 1, num_samples) * sample_time
                ax.plot(timestamps, plot)
            ax.set_xlabel(sample_time_unit)
            ax.set_ylabel("mV")
            ax.set_xlim(0, sample_time)
            ax.set_ylim(0, visible_plot.v_ref)
            self.draw()
