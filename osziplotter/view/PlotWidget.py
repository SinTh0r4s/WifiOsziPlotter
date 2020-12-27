from osziplotter.Util import get_frequency_readable, get_timestamp_readable
from osziplotter.modelcontroller.PlotEvents import PlotEvents
from osziplotter.modelcontroller.PlotInfo import PlotInfo

from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from typing import Dict
import numpy as np


class PlotWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(PlotWidget, self).__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self, width=10, height=8)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)


class PlotCanvas(FigureCanvasQTAgg, PlotEvents):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def update_plot(self, plots: Dict[float, PlotInfo], visible_plot: PlotInfo = None) -> None:
        self.figure.clf()
        if visible_plot is not None:
            ax = self.figure.add_subplot(111)
            ax.set_title("Samples taken at " + get_timestamp_readable(visible_plot.timestamp))
            ax.hold(True)
            for channel in visible_plot.channels:
                plot = visible_plot.channels[channel]
                num_samples = len(plot)
                timestamps = np.linspace(0, num_samples-1, num_samples) / visible_plot.frequency
                ax.plot(timestamps, plot)
            ax.hold(False)
            (frequency, frequency_unit) = get_frequency_readable(visible_plot.frequency)
            ax.set_xlabel(frequency_unit)
            ax.set_ylabel("mV")
            ax.set_xlim(0, visible_plot.num_samples / visible_plot.frequency)
            ax.set_ylim(0, visible_plot.v_ref)
            self.draw()
