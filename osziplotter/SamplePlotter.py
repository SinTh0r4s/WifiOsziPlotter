# lib imports
from tkinter import Frame, TOP, BOTH
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import numpy as np

# local imports
from osziplotter.modelcontroller.BoardInfo import BoardInfo


class SamplePlotter(Frame):

    def __init__(self, master):
        Frame.__init__(self, master=master)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.artist = None
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)

        def on_key_press(event):
            key_press_handler(event, self.canvas, self.toolbar)
        self.canvas.mpl_connect("key_press_event", on_key_press)

    def refresh(self, info: BoardInfo, samples: np.array):
        x_data = np.arange(0, info.sample_time, info.sample_time / info.num_samples)  # TODO: better to adjust to sample vector length
        self.artist, = self.plot.plot(x_data, samples)
        self.plot.set_xlabel(info.sample_time_unit)
        self.plot.set_ylabel("mV")
        self.plot.set_xlim(0, info.sample_time)
        self.plot.set_ylim(0, info.v_ref)
        self.canvas.draw()
        self.toolbar.update()

    def reset(self):
        if self.artist is not None:
            self.artist.remove()
            self.artist = None
